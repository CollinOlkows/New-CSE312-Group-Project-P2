feed_start()
function make_post() {
    const disc = document.getElementById("post_content");
    const post_disc = disc.value;
    const Title = document.getElementById("Title");
    const t_value = Title.value;
    
        // Using AJAX
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response);
                //location.reload();
            }
        }
        const messageJSON = {"content": post_disc,"title":t_value};
        request.open("POST", "/post");
        request.setRequestHeader("Content-type", "application/json; charset=utf8");
        request.send(JSON.stringify(messageJSON));
}

function like_post(post_id) {
    const like_value = document.getElementById("like_button_"+String(post_id));
    
        // Using AJAX
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(JSON.parse(this.response));
                data = JSON.parse(this.response)
                like_value.value=data['emoji']+data['likes']
            }
        }
        const messageJSON = {'post_id':post_id};
        request.open("POST", "/like_post");
        request.setRequestHeader("Content-type", "application/json; charset=utf8");
        request.send(JSON.stringify(messageJSON));
}

function AddPost(post){
    let container = document.getElementById('All_Posts_Container')
    // insert post at the beginning of container
}

function updateChat() {
    let time = document.getElementById('time').value
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(JSON.parse(this.response));
            const posts = JSON.parse(this.response);
            for (const post of posts) {
                console.log(post);
                AddPost(post);
            }
        }
    }
    const messageJSON = {'time':time};
    request.open("POST", "/get_posts");
    request.setRequestHeader("Content-type", "application/json; charset=utf8");
    request.send(JSON.stringify(messageJSON));
}

function feed_start(){
    updateChat();
    setInterval(updateChat, 2000);
}