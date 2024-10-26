<script>
	import { goto } from '$app/navigation';

	let tweets = [
		{
			id: 1,
			img: 'https://i.kym-cdn.com/photos/images/original/002/130/917/d0f.png',
			date: '00:00 AM · Jan 01, 2021',
			retweets: '500k Retweets',
			quoteTweets: '100k Quote Tweets',
			likes: '1M Likes'
		},
		{
			id: 2,
			img: 'https://compote.slate.com/images/926e5009-c10a-48fe-b90e-fa0760f82fcd.png?crop=680%2C453%2Cx0%2Cy0',
			date: '00:00 AM · Jan 01, 2022',
			retweets: '100k Retweets',
			quoteTweets: '50k Quote Tweets',
			likes: '300k Likes'
		},
		{
			id: 3,
			img: 'https://www.thebalancemoney.com/thmb/2DWYDrQIRgaiCJibOskzLvB-Od0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/confusedstonks-cb743905a15b41ada79d4d3e4ecb5b94.jpg',
			date: '00:00 AM · Jan 01, 2023',
			retweets: '150k Retweets',
			quoteTweets: '59k Quote Tweets',
			likes: '350k Likes'
		}
	];

	let stockName = '[Stock name]';

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
			/>
		</div>
		<div class="grid grid-cols-10 grid-rows-10 w-full h-4/5 border border-black m-auto">
			{#each Array(100) as _, i}
				<div class="border border-gray-300"></div>
			{/each}
		</div>
	</div>
	<div class="flex-[3] flex flex-col overflow-y-auto pr-5">
		<!-- Adjusted flex to 1.5 -->
		{#each tweets as tweet (tweet.id)}
			<div class="bg-white border border-gray-300 p-4 m-2 rounded-lg">
				<div class="flex items-center mb-4">
					<img
						src="https://via.placeholder.com/50"
						alt="Profile Picture"
						class="rounded-full mr-3"
					/>
					<div>
						<div>John Doe</div>
						<div>@johndoe</div>
					</div>
				</div>
				<div class="tweet-content">
					<img src={tweet.img} alt="Tweet Image" class="max-w-full h-auto rounded-lg" />
				</div>
				<div class="flex justify-between mt-4 text-sm text-gray-600">
					<div>{tweet.date}</div>
					<div>
						<span>{tweet.retweets}</span> |
						<span>{tweet.quoteTweets}</span> |
						<span>{tweet.likes}</span>
					</div>
				</div>
			</div>
		{/each}
	</div>
	<div
		class="w-3 bg-gradient-to-b from-green-400 to-red-600 absolute right-5 top-0 bottom-0 my-auto"
	></div>
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
		margin-left: 50px; /* Adjusted margin for gap */
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
</style>
