
// function to send JSON Http post request
function sendJSONHTTPPost(url, objects, callback){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState==4) {
            try {
                if (xhr.status==200) {
                    callback(xhr.response);
                }
            } 
            catch(e) {
                alert('Error: ' + e.name);
            }
        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("POST", "http://"+url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send(JSON.stringify(objects));
    
}

// callback function after sending friend request
// - Simply change the "befriend" button to "unfriend" button
function sendFriendRequestCallback(objects){
    var btn = document.getElementById("btn-befriend");
    btn.style.display = "none";

    var new_btn = document.getElementById("btn-unfriend");
    new_btn.style.display = "block";
}

// callback function after sending unfriend request
// - Simply change the "unfriend" button to "befriend" button
function sendUnFriendRequestCallback(objects){
    var btn = document.getElementById("btn-unfriend");
    btn.style.display = "none";
    var new_btn = document.getElementById("btn-befriend");
    new_btn.style.display = "block";
}

// function to send befriend request
function sendFriendRequest(init, recv){
    users = {"query": "friendrequest", "author": init, "friend": recv};
    sendJSONHTTPPost(recv.host+"/api/friendrequest/", users, sendFriendRequestCallback);
}

// function to send unfriend request
function sendUnFriendRequest(init, recv){
    users = {"query": "unfriendrequest", "author": init, "friend": recv};
    sendJSONHTTPPost(recv.host+"/api/unfriendrequest/", users, sendUnFriendRequestCallback);
}

// callback function after sending init
// - Simply change the button to "unfriend" if they are friends
function sendInitRequestCallback(response){
    var response = JSON.parse(response);
    if(response.authors.length == 0){
        var btn = document.getElementById("btn-unfriend");
        btn.style.display = "none";
        var new_btn = document.getElementById("btn-befriend");
        new_btn.style.display = "block";
    }else{
        var btn = document.getElementById("btn-befriend");
        btn.style.display = "none";
        var new_btn = document.getElementById("btn-unfriend");
        new_btn.style.display = "block";
    }
}


// function to initialize profile page based on if current user and the user he is viewing are friends or not.
function init_profile_page(init, recv){
    request_body = {'authors':"['"+recv.id+"']"};
    sendJSONHTTPPost(init.host+"/api/author/"+init.id+"/following/", request_body, sendInitRequestCallback);
}
