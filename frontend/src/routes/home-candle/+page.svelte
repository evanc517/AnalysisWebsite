<script>
    var stock = "";

    function onSubmit() {
        window.location.href = "http://localhost:3000/candlesticks?asset=" + stock;
    };
</script>
<body>
    <style>
        body{
            background-image: url('backgroundv2.png');
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: 100% 100%;
        }
    </style>
    
    
    <div class="flex items-start">
        <a href="http://localhost:3000/home-candle">
            <button><img src="logo.png" alt="stair.ai" width="130"></button>
        </a>
    
        <!--Sentiment button-->
        <a href="http://localhost:3000/">
            <button><img src="sentiment.png" alt="Sentiment button" width="140"></button>
        </a>
        
        <a href="http://localhost:3000/home-candledark">
            <button><img src="dark.png" alt="Dark mode" width="150"></button>
        </a>
    </div>
    
    <div class="flex flex-col fixed inset-14 flex items-center justify-center">
        <br><br><br><br><br>
        <p style="color:gray;"><i>DISCLAIMER:This site uses AI modeling for its predictions and should not be taken as the truth.</i></p>
    </div>
    
    <div class="flex flex-col fixed inset-14 flex items-center justify-center">
        <div class="text-5xl">
            <label for="stock">Step up to Analyze</label>
        </div><br>
        <form on:submit={e => e.preventDefault()} class="mb-10">
        <div class="text-4xl">
            <input type="text" style="background-color:#d8d8d8" id="stock" name="stock" placeholder="Enter Financial Asset" value={stock} on:change={e => stock = e.target.value}>
            <button class = "px-1 bg-gray-500 text-white" on:click={onSubmit}>Enter</button>
        </div>
    </div>
    
    <div class="absolute bottom-0 right-0">
        <a href="http://localhost:3000/about-light">
            <button><img src="about.png" alt="about" width="100"></button>
        </a>
    </div>
    
    </body>
