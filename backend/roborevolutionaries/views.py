from django.shortcuts import render
import yfinance as yf
import pandas as pd
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from yahooquery import search
from bs4 import BeautifulSoup
import tensorflow as tf
import time
import numpy as np
import logging
from rest_framework import status
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

model = tf.saved_model.load('roborevolutionaries/models/sentiment_model')
stockmodel = tf.saved_model.load('roborevolutionaries/models/stock_model')
#candlestick_model = tf.keras.models.load_model("roborevolutionaries/models/candlestick.keras")

# Set up logging
logger = logging.getLogger(__name__)

# In-memory cache for ticker symbols
ticker_cache = {}


@api_view(["POST"])
def sentiment(request):
    def fetch_company_info(ticker_symbol):
        ticker_symbol = ticker_symbol.upper()
        try:
            results = search(ticker_symbol)
            if results['quotes']:
                return results['quotes'][0]['longname'], results['quotes'][0]['symbol'] == ticker_symbol
        except Exception:
            return None, False
        return None, False

    def fetch_image_links(images):
        placeholder_url = "https://www.projectactionstar.com/uploads/videos/no_image.gif"
        return [
            image.get(attr) if "logo" not in (image.get(attr) or "").lower() and "data:image" not in (image.get(attr) or "")
            else placeholder_url
            for image in images
            for attr in ["data-srcset", "data-src", "data-fallback-src", "src"]
            if image.get(attr)
        ]

    if request.method == 'POST':
        asset = request.data.get('asset')

        asset, valid_ticker = fetch_company_info(asset) if asset else (None, False)
        if not asset:
            return Response({'status': 404, 'message': 'could not fetch name'})

        asset = asset.title()
        all_news, all_images = [], []
        num_pages = 5

        for page in range(num_pages):
            time.sleep(0.1)
            url = f'https://news.search.yahoo.com/search?p={asset}&b={page * 10 + 1}'
            response = requests.get(url)

            if response.status_code != 200:
                return Response({'status': 404, 'message': 'could not fetch news'})

            soup = BeautifulSoup(response.text, 'html.parser')
            for news_item in soup.find_all('div', class_='NewsArticle'):
                title = news_item.find('h4').text.strip()
                all_news.append(title)
                all_images.extend(fetch_image_links(soup.findAll('img')))
                if len(all_news) >= 20:
                    break
            if len(all_news) >= 20:
                break

        all_news = list(dict.fromkeys(all_news))[:20]
        all_images = list(dict.fromkeys(all_images))[:20]

        dif = len(all_news) - len(all_images)

        for _ in range(dif):
            all_images.append("https://www.projectactionstar.com/uploads/videos/no_image.gif")

        try:
            predictions = model(tf.constant(all_news)).numpy().tolist()
            avg = sum((prediction[0] if prediction[0] > 0.5 else -1 * (1 - prediction[0])) for prediction in predictions) / len(predictions)
            response = {
                'status': 200,
                'avg_score': float('%.3f' % avg),
                'news': all_news,
                'images': all_images,
                'scores': [float('%.3f' % (prediction[0] if prediction[0] > 0.5 else -1 * (1 - prediction[0]))) for prediction in predictions],
            }
        except Exception:
            return Response({'status': 400, 'message': 'something went wrong'})

        return Response(response)

@api_view(["POST"])
def history_view(request):
    try:
        company_name = request.data.get("asset")

        if not company_name:
            return Response({
                "status": 404,
                "error": "Unable to find price history for financial asset."
            }, status=404)

        ticker = get_ticker_from_company_name(company_name)

        if not ticker:
            return Response({
                "status": 404,
                "error": "Unable to find ticker for the given company name."
            }, status=404)

        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")

        if data.empty:
            return Response({
                "status": 404,
                "error": "No historical data found for the ticker."
            }, status=404)

        # Ensure 'Adj Close' is available
        if 'Adj Close' not in data.columns:
            data['Adj Close'] = data['Close']

        # Calculate technical indicators
        data['RSI'] = ta.rsi(data['Close'], length=15)
        data['EMAF'] = ta.ema(data['Close'], length=20)
        data['EMAM'] = ta.ema(data['Close'], length=100)
        data['EMAS'] = ta.ema(data['Close'], length=150)
        data['EMA'] = ta.ema(data['Close'], length=200)

        # Create target columns
        data['Target'] = data['Adj Close'] - data['Open']
        data['TargetNextClose'] = data['Adj Close'].shift(-1)

        # Drop rows with NaN values only after calculations
        data.dropna(subset=['RSI', 'EMAF', 'EMAM', 'EMAS', 'EMA', 'Target', 'TargetNextClose'], inplace=True)

        # Prepare input features for prediction
        feature_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'RSI', 'EMAF', 'EMAM', 'EMAS', 'EMA']
        if len(data) < 30:  # Ensure there's enough data to reshape
            return Response({
                "status": 404,
                "error": "Not enough data to make prediction."
            }, status=404)

        last_data = data[feature_columns].values[-30:]  # Get the last 30 time steps
        input_tensor = np.reshape(last_data, (1, 30, 11)).astype(np.float32)  # Ensure input is float32
        preds = stockmodel(tf.convert_to_tensor(input_tensor, dtype=tf.float32))

        # Convert preds to a list
        preds_list = preds.numpy().flatten().tolist()

        # Prepare prediction dates
        pred_dates = [(pd.to_datetime(data.index[-1]) + pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 15)]

        response = {
            "status": 200,
            "ticker": ticker,
            "preds": preds_list,
            "pred_dates": pred_dates,
        }
        return Response(response)

    except Exception as e:
        return Response({
            "status": 500,
            "error": str(e),
        }, status=500)





def get_ticker_from_company_name(company_name):
    try:
        results = search(company_name)  # Directly use the result
        if results['quotes']:
            return str(results['quotes'][0]['symbol'])
    except Exception as e:
        print(f"Error in get_ticker_from_company_name: {e}")
        return None  # Return None on any error
    return None  # Return None if no quotes found

        
@api_view(["POST"])
def candlestick_view(request):
    try:
        company_name = request.data.get("company_name")

        if not company_name:
            return Response({
                "status": 400,
                "error": "Company name not provided."
            }, status=400)
        
        ticker = get_ticker_from_company_name(company_name)

        if not ticker:
            return Response({
                "status":404,
                "error": "unable to find ticker for given company name."
            }, status=404)
        
        stock = yf.Ticker(ticker)
        data = stock.history(period="3mo")


        data = data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)

        date = data.index[-1]

        closing_prices = data['Close'].values.reshape(-1, 1)
        high_prices = data['High'].values.reshape(-1, 1)
        low_prices = data['Low'].values.reshape(-1, 1)
        open_prices = data['Open'].values.reshape(-1, 1) 

        scaler = MinMaxScaler(feature_range=(0, 1))
        closing_prices = scaler.fit_transform(closing_prices)
        high_prices = scaler.fit_transform(high_prices)
        low_prices = scaler.fit_transform(low_prices)
        open_prices = scaler.fit_transform(open_prices)

        
        scaled_data = np.hstack((closing_prices, high_prices, low_prices, open_prices))


        predicted_prices = []
        current_batch = scaled_data[-30:].reshape(1, 30, 4)  # Most recent 30 days

        data = data[-30:]
        for i in range(14):  # Predicting 4 days
            # Get the prediction (next day)
            next_prediction = candlestick_model.predict(current_batch)

            # Reshape the prediction to fit the batch dimension
            next_prediction_reshaped = next_prediction.reshape(1, 1, 4)

            # Append the prediction to the batch used for predicting
            current_batch = np.append(current_batch[:, 1:, :], next_prediction_reshaped, axis=1)

            # Inverse transform the prediction to the original price scale
            predictions = scaler.inverse_transform(next_prediction)[0]
            new_date = date + timedelta(days=i + 1)

            df = [
            {'Date': new_date, 'Open': predictions[3], 'High': predictions[1], 'Low': predictions[2], 'Close': predictions[0]},
            ]

            df = pd.DataFrame(df)

            # Set 'Date' as the index
            df.set_index('Date', inplace=True)

            data = pd.concat([data, df], ignore_index=False)

        data_dict = data.to_dict(orient='list')

        response = {
            "status": 200,
            "ticker": ticker,
            "data": data_dict
        }
        return Response(response)

    
    except Exception as e:
        response = {
            "status":500,
            "error": str(e),
        }
        return Response(response, status=500)
