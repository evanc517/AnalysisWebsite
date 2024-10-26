<script>
	let src = 'src/assets/image.gif';
	let name = 'Rick Astley';

	function goBack() {
		window.location.href = '/home-light';
	}
</script>

<div class="header-container">
	<div class="background-rectangle"></div>
	<h1 class="header-content text-center text-3xl font-bold text-white">About</h1>
</div>

<button on:click={goBack} class="text-white px-4 py-2 rounded absolute top-9 left-4">
	&lt; Back
</button>

<div class="footer-container"></div>

<p style="text-align: center; font-size: 1.15rem;" class="text-black text-lg">
	Stair.AI is a website where you can find out the sentiment of any financial asset! With a click of
	a button you can see the sentiment of stocks, crypto, mutual funds and more.
</p>
<p style="text-align: center; font-size: 1.2rem;" class="text-black text-lg">
	This website is written by members of <a
		href="https://ai-camp.org"
		style="font-size: 1.2rem; color:blue;">ai-camp.org</a
	>!
</p>

<p class="font-bold text-center text-White-600 mt-20">Frontend Team</p>

<div class="flex justify-center justify-around">
	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Alex</figcaption>
	</figure>

	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Ethan</figcaption>
	</figure>

	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Evan</figcaption>
	</figure>
</div>

<p class="font-bold text-center text-White-600 mt-20">Backend Team</p>

<div class="flex justify-center justify-evenly">
	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Jacob</figcaption>
	</figure>

	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Andres</figcaption>
	</figure>

	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Chris</figcaption>
	</figure>

	<figure class="text-center w-32">
		<img class="w-full" src="/usericon.png" alt="icon" />
		<figcaption>Amaresh</figcaption>
	</figure>
</div>

<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"><img {src} alt="{name} dancing" /></a>

<style>
	.header-container {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 20px;
		padding: 20px;
	}

	.background-rectangle {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(180deg, rgb(207, 30, 23), rgb(255, 99, 71));
		z-index: -1;
	}

	.header-content {
		position: relative;
		z-index: 1;
	}

	.footer-container {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		padding: 20px;
		background: linear-gradient(180deg, rgb(0, 128, 0), rgb(47, 237, 39));
		color: white;
		text-align: center;
	}
</style>
