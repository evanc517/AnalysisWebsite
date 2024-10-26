<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let stockName = '';
	let news = [];
	let sentiment = {};
	let priceHistory = [];
	let priceHistoryError = '';

	onMount(async () => {
		const params = new URLSearchParams(window.location.search);
		const asset = params.get('asset') || '[Stock name]';
		stockName = asset;

		try {
			const sentimentResponse = await fetch(`/sentiment?asset=${asset}`);
			const sentimentData = await sentimentResponse.json();
			news = sentimentData.news;
			sentiment = sentimentData.sentiment;
		} catch (error) {
			console.error('Error fetching sentiment data:', error);
		}

		try {
			const historyResponse = await fetch(`/history?asset=${asset}`);
			if (!historyResponse.ok) throw new Error('Failed to fetch price history');
			priceHistory = await historyResponse.json();
		} catch (error) {
			priceHistoryError = `Cannot get price history for: ${asset}`;
			console.error('Error fetching price history:', error);
		}
	});

	function goBack() {
		goto('/home-light');
	}
</script>

<div class="flex h-screen p-5 bg-white text-black">
	<div class="flex-[4] flex flex-col relative">
		<div class="flex items-center mb-5">
			<button
				class="absolute left-0 text-lg cursor-pointer bg-transparent border-none"
				on:click={goBack}>&lt; Back</button
			>
			<input
				type="text"
				bind:value={stockName}
				class="ml-24 text-2xl font-bold border-none outline-none bg-transparent"
				readonly
			/>
		</div>
		<div
			class="graph-container grid grid-cols-10 grid-rows-10 w-full h-4/5 border border-black m-auto relative"
		>
			{#if priceHistoryError}
				<div
					class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 pointer-events-auto"
				>
					<p class="text-xl font-bold">{priceHistoryError}</p>
				</div>
			{:else}
				{#each priceHistory as price, i}
					<div class="border border-gray-300">{price}</div>
				{/each}
			{/if}
		</div>
	</div>
	<div class="flex-[3] flex flex-col overflow-y-auto pr-5">
		<div
			class="bg-white border border-gray-300 p-4 m-2 rounded-lg flex items-center justify-center h-full"
		>
			<img
				src="https://via.placeholder.com/550x300"
				alt="Placeholder"
				class="max-w-full h-auto rounded-lg"
			/>
		</div>
		<div
			class="bg-white border border-gray-300 p-4 m-2 rounded-lg flex items-center justify-center h-full"
		>
			<img
				src="https://via.placeholder.com/550x300"
				alt="Placeholder"
				class="max-w-full h-auto rounded-lg"
			/>
		</div>
		<div
			class="bg-white border border-gray-300 p-4 m-2 rounded-lg flex items-center justify-center h-full"
		>
			<img
				src="https://via.placeholder.com/550x300"
				alt="Placeholder"
				class="max-w-full h-auto rounded-lg"
			/>
		</div>
	</div>
	<div
		class="w-3 bg-gradient-to-b from-green-400 to-red-600 absolute right-5 top-0 bottom-0 my-auto"
	>
		<!-- Sentiment arrowhead at TEMPORARY POSITION-->
		<div
			class="arrowhead absolute left-0 -translate-x-full top-1/2 transform -translate-y-1/2"
		></div>
	</div>
</div>

<style>
	.container {
		display: flex;
		height: 100vh;
		padding: 20px;
		color: black;
		background-color: white;
	}

	.left-panel {
		flex: 4;
		display: flex;
		flex-direction: column;
		position: relative;
	}

	.grid {
		width: 100%;
		height: 80%;
		display: grid;
		grid-template-columns: repeat(10, 1fr);
		grid-template-rows: repeat(10, 1fr);
		border: 1px solid black;
		margin: auto;
	}

	.grid div {
		border: 1px solid lightgray;
	}

	.right-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow-y: auto;
	}

	.header {
		display: flex;
		align-items: center;
		margin-bottom: 20px;
	}

	.back-button {
		background-color: transparent;
		border: none;
		color: black;
		font-size: 16px;
		cursor: pointer;
		position: absolute;
		left: 0;
	}

	.stock-name {
		font-size: 24px;
		font-weight: bold;
		margin-left: 50px;
	}

	.tweet {
		background-color: white;
		border: 1px solid #ccc;
		padding: 15px;
		margin: 10px;
		border-radius: 8px;
	}

	.tweet-header {
		display: flex;
		align-items: center;
	}

	.tweet-header img {
		border-radius: 50%;
		margin-right: 10px;
	}

	.tweet-content img {
		max-width: 100%;
		height: auto;
		border-radius: 8px;
	}

	.tweet-footer {
		display: flex;
		justify-content: space-between;
		margin-top: 10px;
	}

	.slider {
		width: 10px;
		background: linear-gradient(to bottom, #2fed27, #ff2727);
		position: absolute;
		right: 75px;
		top: 0;
		bottom: 0;
		margin: auto;
	}

	.graph-container .pointer-events-auto {
		pointer-events: auto;
	}

	.arrowhead {
		width: 0;
		height: 0;
		border-left: 10px solid black;
		border-top: 5px solid transparent;
		border-bottom: 5px solid transparent;
	}
</style>
