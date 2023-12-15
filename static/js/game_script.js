
function start_game(){
//document.querySelector('html').innerHTML = '<html><head><link  rel="stylesheet" href="/css/style.css"><link  rel="stylesheet" href="/css/lobby.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.0.4/socket.io.js" integrity="sha512-aMGMvNYu8Ue4G+fHa359jcPb1u+ytAF+P2SCb+PxrjCdO3n3ZTxJ30zuH39rimUggmTwmh2u7wvQsDTHESnmfQ==" crossorigin="anonymous"></script></head>  <body><div id="Game_Board"><h1>Scoreboard</h1><div id="user_list"><p>🟢William: 0</p><p>🔴Joe: 0</p><p>⚖️Johnny: 0</p><p>🔴Daniel: 0</p><p>🔴Rob: 0</p></div><div><h1>Johnny is Judging!</h1><img src="/catalog/logo.png" style="height: 5vmax; width: 5vmax;"></div><div><h2>Type Your Prompt Below!</h2><input type="text" placeholder="Prompt"><button>Submit Prompt!</button></div></div></body></html>';
document.getElementById('Game_Board').innerHTML = '<h1>Scoreboard</h1><div id="user_list"><p>🟢William: 0</p><p id="Joe">🔴Joe: 0</p><p>⚖️Johnny: 0</p><p>🔴Daniel: 0</p><p>🔴Rob: 0</p></div><div><h1>Johnny is Judging!</h1><img src="/catalog/logo.png" style="height: 5vmax; width: 5vmax;"></div><div id="prompt_div"><h2>Type Your Prompt Below!</h2><input type="text" placeholder="Prompt" id="prompt"><button onclick="submit_prompt()">Submit Prompt!</button></div>'

}

function submit_prompt(){
    let prompt = document.getElementById('prompt').value;
    console.log(prompt)
    document.getElementById('prompt_div').innerHTML = '<button onclick="judge_prompts();">Judging Screen</button><button onclick="Please_Wait();">Wait</button>'
    document.getElementById('Joe').innerHTML='🟢Joe: 0'
}

function judge_prompts(){
    document.getElementById('Game_Board').innerHTML = '<h1>Scoreboard</h1><div id="user_list"><p>🟢William: 0</p><p>🟢Joe: 0</p><p>⚖️Johnny: 0</p><p>🟢Daniel: 0</p><p>🟢Rob: 0</p></div><div id ="image"><h1>Johnny is Judging!</h1><img src="/catalog/logo.png" style="height: 5vmax; width: 5vmax;"></div><div id="Prompt"><button onclick="display_scoreboard()">Chicken</button><button onclick="display_scoreboard()">Prompt2</button><button onclick="display_scoreboard()">William Bozo</button><button onclick="display_scoreboard()">IDk stuff</button><button onclick="display_scoreboard()">Other Stuff</button></div></div>'
}

function Please_Wait(){
    document.getElementById('prompt_div').innerHTML = '<p>Please Wait For Other Players to Submit</p>'
}

function display_scoreboard(){
    document.getElementById('Game_Board').innerHTML = '<h1>Scoreboard</h1><div id="user_list"><p>William: 6</p><p>Joe: 3</p><p>Johnny: 2</p><p>Daniel: 1</p><p>Rob: 1</p></div>'
}
