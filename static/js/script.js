function make_post() {
    const disc = document.getElementById("post_content");
    const post_disc = chatTextBox.value;
    const Title = document.getElementById("Title");
    disc.value = "";
    const t_value = Title.value;
    Title.value = "";
    
        // Using AJAX
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response);
            }
        }
        const messageJSON = {"content": post_disc,'title':t_value};
        request.open("POST", "/post");
        request.send(JSON.stringify(messageJSON));
        disc.focus();
        location.reload();
}

function like_post(post_id) {
    const like_value = document.getElementById("like_button_"+String(post_id));
    
        // Using AJAX
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(JSON.parse(this.response));
                //update post value and char
            }
        }
        const messageJSON = {'post_id':post_id};
        request.open("POST", "/like_post");
        request.send(JSON.stringify(messageJSON));
}