


function start_game(players,judge, user,img){
    ply = true
    if(judge == user){
        game_string = '<div id="prompt_div" class="GIPprompt"><h2 class="GIPpromptTitle">You are the judge. Please wait for all players to submit</h2></div><br><div class="GIPgameContainer"><div class="GIPscoreBoard"><h1>SCOREBOARD</h1><div class="GIPscoreBoardContainer"><div id="user_list">'
        ply = false
    }else{
    game_string = '<div id="prompt_div" class="GIPprompt"><h2 class="GIPpromptTitle">TYPE YOUR PROMPT BELOW</h2><textarea id="promptInput" class="GIPpromptForm" maxlength="300" placeholder="Prompt"></textarea><button class="GIPpromptSubmit" id="prompt_submit">SUBMIT YOUR PROMPT</button></div><br><div class="GIPgameContainer"><div class="GIPscoreBoard"><h1>SCOREBOARD</h1><div class="GIPscoreBoardContainer"><div id="user_list">'
    }
    let i = 0;
    while (i < players.length) {
        if(players[i]['username']==judge){
            game_string += '<p id='+ players[i]['username'] + '>' + '⚖️'+ players[i]['username'] + ': '+String(players[i]['score'])+'</p>'
        }else{
            game_string += '<p id='+ players[i]['username'] + '>' + '🔴'+ players[i]['username'] + ': '+String(players[i]['score'])+'</p>'
        }
        i++;
    }
    game_string+='</div></div></div><div class="GIPjudge"><h1>JUDGING</h1><div class="GIPjudgeContainer"><h2 id="judge_name">CockusBallus</h2><img id="current_image" src="/static/images/lebronDuck.jpeg" class="GIPjudgeImg"></div></div></div><script>$(document).ready(function() {$("#promptInput").on("input", function() {this.style.height = "auto";this.style.height = (this.scrollHeight) + "px";});});</script>'
//document.querySelector('html').innerHTML = '<html><head><link  rel="stylesheet" href="/css/style.css"><link  rel="stylesheet" href="/css/lobby.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.0.4/socket.io.js" integrity="sha512-aMGMvNYu8Ue4G+fHa359jcPb1u+ytAF+P2SCb+PxrjCdO3n3ZTxJ30zuH39rimUggmTwmh2u7wvQsDTHESnmfQ==" crossorigin="anonymous"></script></head>  <body><div id="Game_Board"><h1>Scoreboard</h1><div id="user_list"><p>🟢William: 0</p><p>🔴Joe: 0</p><p>⚖️Johnny: 0</p><p>🔴Daniel: 0</p><p>🔴Rob: 0</p></div><div><h1>Johnny is Judging!</h1><img src="/catalog/logo.png" style="height: 5vmax; width: 5vmax;"></div><div><h2>Type Your Prompt Below!</h2><input type="text" placeholder="Prompt"><button>Submit Prompt!</button></div></div></body></html>';
document.getElementById('Game_Board').innerHTML = game_string
if(ply){
    document.getElementById('prompt_submit').addEventListener("click", submit_the_prompt);
}
document.getElementById('judge_name').innerHTML=judge
document.getElementById('current_image').src =img

}



function judge_prompts(){
    document.getElementById('Game_Board').innerHTML = '<h1>Scoreboard</h1><div id="user_list"><p>🟢William: 0</p><p>🟢Joe: 0</p><p>⚖️Johnny: 0</p><p>🟢Daniel: 0</p><p>🟢Rob: 0</p></div><div id ="image"><h1>Johnny is Judging!</h1><img src="/catalog/logo.png" style="height: 5vmax; width: 5vmax;"></div><div id="Prompt"><button onclick="display_scoreboard()">Chicken</button><button onclick="display_scoreboard()">Prompt2</button><button onclick="display_scoreboard()">William Bozo</button><button onclick="display_scoreboard()">IDk stuff</button><button onclick="display_scoreboard()">Other Stuff</button></div></div>'
}

function Please_Wait(){
    document.getElementById('prompt_div').innerHTML = '<p>Please Wait For Other Players to Submit</p>'
}

function Please_Wait_on_judge(){
    document.getElementById('prompt_div').innerHTML = '<p>Please Wait For The Judge to choose the winner</p>'
}

function display_scoreboard(){
    document.getElementById('Game_Board').innerHTML = '<h1>Scoreboard</h1><div id="user_list"><p>William: 6</p><p>Joe: 3</p><p>Johnny: 2</p><p>Daniel: 1</p><p>Rob: 1</p></div>'
}

function render_judge_page(players,image,judge){
    game_string = '<div class="GRjudge"><h1>YOU ARE JUDING</h1><h2>ROUND IMAGE</h2><img id="current_image" src="/static/images/packs/willPack/BingImage14.jpeg" class="GRpromptImg"></div><div id="prompt_div" class="GRPrompt"><h1 class="GRpromptTitle">PROMPTS</h1><h2 class="GRpromptDirections">PICK THE PROMPT THAT YOU THINK IS THE BEST</h2>'

    let j = 0;
    while (j < players.length) {
        if(players[j]['username']!=judge){
            console.log(players[j]['input'])
        game_string+='<button class="GRpromptPromptsButtons"'+' id="'+players[j]['username']+'"'+'onclick="prompt_win('+"'"+players[j]['username']+"'"+')">'+players[j]['input']+'</button>'
        }
        j++;
    }
    game_string +='</div></div><br><div><h1 class="GRscoreBoardTitle">SCORE BOARD</h1><div id="user_list" class="GRscoreBoardForm">'

    let i = 0;
    while (i < players.length) {
        if(players[i]['username']==judge){
            game_string += '<p id='+ '"'+players[i]['username'] + '"' + ' class="GRscoreBoardRankings">' + '⚖️'+ players[i]['username'] + ': '+String(players[i]['score'])+'</p>'
        }else{
            game_string += '<p id='+ '"'+players[i]['username'] + '"' + ' class="GRscoreBoardRankings">' + '🟢'+ players[i]['username'] + ': '+String(players[i]['score'])+'</p>'
        }
        i++;
    }
    game_string+='</div></div>'
    document.getElementById('Game_Board').innerHTML = game_string
    document.getElementById('current_image').src =image
}

function show_prompts_to_players(players,winner,judge,user){
    let j = 0;
    game_string = '<h1 class="GRpromptTitle">PROMPTS</h1>'
    scores = ''
    je = false
    if (user == judge){
        je = true
    }
    while (j < players.length) {
        if(players[j]['username']!=judge){
            if(players[j]['username']==winner){
                game_string+='<button class="GRpromptPromptsButtons GRwinner"'+' id="'+players[j]['username']+'">'+players[j]['username']+':'+players[j]['input']+'</button>'
            }else{
                game_string+='<button class="GRpromptPromptsButtons"'+' id="'+players[j]['username']+'">'+players[j]['username']+':'+players[j]['input']+'</button>'
            }
            scores += '<p id='+ '"'+players[j]['username'] + '"' + ' class="GRscoreBoardRankings">' + '🟢'+ players[j]['username'] + ': '+String(players[j]['score'])+'</p>'
        }else{
            scores += '<p id='+ '"'+players[j]['username'] + '"' + ' class="GRscoreBoardRankings">' + '⚖️'+ players[j]['username'] + ': '+String(players[j]['score'])+'</p>'
        }

        j++;
    }
    if(je){
        game_string += '<button onclick="next_turn()">Continue Game</button>'
        document.getElementById('prompt_div').innerHTML = game_string
    }else{
        document.getElementById('prompt_div').innerHTML = game_string
    }
    document.getElementById('user_list').innerHTML = scores
}

function show_scores(host,players){
    game_string='<div class="users"><h1>Scores</h1><div id="User_List" class="userList">'
    let i = 0;
    while (i < players.length) {
        game_string += '<p id='+ players[i]['username'] + '>' + ''+ players[i]['username'] + ': '+String(players[i]['score'])+'</p>'
        i++;
    }
    if(host){
        game_string+='<button onclick="End_The_Game();">End Game</button>'
    }
    game_string+='</div></div>'
    document.getElementById('Game_Board').innerHTML = game_string
}