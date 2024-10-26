# robo-revolutionaries
<hr>

## Setup
### Frontend
- Navigate to the `frontend` folder
- Run the following command:
```
npm install
```
- To run the frontend, execute: `npm run dev`

### Backend
- Create a python virtual environment named `env`
```
python -m venv env
```
- Activate the virtual environment
- Navigate to the `backend` folder
- Run the following commands:
```
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser
```
- To run the backend, execute: `python manage.py runserver`
