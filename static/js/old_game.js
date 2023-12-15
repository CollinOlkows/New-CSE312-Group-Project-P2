<script>
$(document).ready(function(){
    var socket = io({transports: ["websocket"]});
    console.log(socket.io.engine.transport.name)
    socket.on('my response', function(msg) {
        console.log(msg.data)
    });
    function check_value(){
        let a = document.getElementById('a').innerHTML;
        let g = document.getElementById('guess').value;
        if(g == a){
            document.getElementById('msgr').innerHTML='Correct, you win!'
            socket.emit('winner',{'user':'{{user}}','value':a,'lobby':'{{code}}'})
        }else{
            document.getElementById('msgr').innerHTML='Incorrect please guess again'
        }
    }
    socket.emit('update_count', {'lobby': '{{code}}','user':'{{user}}'});
    socket.on('lobby joined',function(msg)  {
        console.log(msg)
    })
    socket.on('lobby_made',function(msg)  {
        console.log(msg)
    })
    socket.on('end_game',function(msg)  {
        alert(msg['user']+' Has won the game. The answer was '+msg['value']+' please return to the main menu to start a new game')
        window.location = '/home-page'
    })
    socket.on('update_users',function(msg)  {
        let un = document.createElement('p');
        un.innerHTML = msg['user']
        document.getElementById('User_List').insertAdjacentElement('afterbegin',un)
        console.log(msg['count'])
        if(msg['max_player']<=msg['count']){
            console.log(msg['game_value'])
            console.log(document.getElementById('a').value)
            document.getElementById('a').value = msg['game_value']
            document.getElementById('a').innerHTML = msg['game_value']
            document.getElementById("User_div").remove()
            let text = document.createElement('p')
            text.innerHTML = 'ender a number 1 - 50'
            document.getElementById("game_make").style.visibility='visible';

            let guess = document.createElement('input')
            guess.id = 'guess'
            guess.placeholder = 'Input Guess'
            let submit = document.createElement('button')
            submit.id='make-guess'
            submit.value = 'Make Guess'
            submit.placeholder = 'Make Guess'
            submit.innerHTML = 'Make Guess'
            submit.addEventListener("click", check_value);
            document.getElementById("game_make").insertAdjacentElement('afterbegin',submit)
            document.getElementById("game_make").insertAdjacentElement('afterbegin',guess)
            document.getElementById("game_make").insertAdjacentElement('afterbegin',text)
        }
    })
});

</script>