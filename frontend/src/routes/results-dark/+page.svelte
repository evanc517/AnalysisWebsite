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
		goto('/home-dark');
	}
</script>

<div class="flex h-screen p-5 bg-[#2b2d31] text-white">
	<div class="flex-[4] flex flex-col relative">
		<div class="flex items-center mb-5">
			<button
				class="absolute left-0 text-lg cursor-pointer bg-transparent border-none text-white"
				on:click={goBack}>&lt; Back</button
			>
			<input
				type="text"
				bind:value={stockName}
				class="ml-24 text-2xl font-bold border-none outline-none bg-transparent text-white"
				readonly
			/>
		</div>
		<div
			class="graph-container grid grid-cols-10 grid-rows-10 w-full h-4/5 border border-gray-600 m-auto relative"
		>
			{#if priceHistoryError}
				<div
					class="absolute inset-0 flex items-center justify-center bg-[#2b2d31] bg-opacity-75 pointer-events-auto text-white"
				>
					<p class="text-xl font-bold">{priceHistoryError}</p>
				</div>
			{:else}
				{#each priceHistory as price, i}
					<div class="border border-gray-600">{price}</div>
				{/each}
			{/if}
		</div>
	</div>
	<div class="flex-[3] flex flex-col overflow-y-auto pr-5">
		<div
			class="bg-gray-800 border border-gray-600 p-4 m-2 rounded-lg flex items-center justify-center h-full"
		>
			<img
				src="https://via.placeholder.com/550x300"
				alt="Placeholder"
				class="max-w-full h-auto rounded-lg"
			/>
		</div>
		<div
			class="bg-gray-800 border border-gray-600 p-4 m-2 rounded-lg flex items-center justify-center h-full"
		>
			<img
				src="https://via.placeholder.com/550x300"
				alt="Placeholder"
				class="max-w-full h-auto rounded-lg"
			/>
		</div>
		<div
			class="bg-gray-800 border border-gray-600 p-4 m-2 rounded-lg flex items-center justify-center h-full"
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
		<!-- Sentiment arrowhead -->
		<div
			class="arrowhead absolute left-0 -translate-x-full top-1/2 transform -translate-y-1/2"
		></div>
	</div>
</div>

<style>
	:global(body) {
		background-color: #2b2d31;
		color: white;
	}

	.container {
		display: flex;
		height: 100vh;
		padding: 20px;
		color: white; /* Changed to white */
		background-color: #2b2d31; /* Changed to #2b2d31 */
	}

	.left-panel {
		flex: 4; /* Adjusted to flex-4 */
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
		border: 1px solid gray; /* Changed to gray */
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
		color: white; /* Changed to white */
		font-size: 16px;
		cursor: pointer;
		position: absolute;
		left: 0;
	}

	.stock-name {
		font-size: 24px;
		font-weight: bold;
		margin-left: 50px; /* Adjusted margin for gap */
	}

	.tweet {
		background-color: gray; /* Changed to gray */
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
		border-left: 10px solid white;
		border-top: 5px solid transparent;
		border-bottom: 5px solid transparent;
	}
</style>
