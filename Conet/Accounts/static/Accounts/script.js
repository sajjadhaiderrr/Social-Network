function sendJSONHTTPPost(url, objects, callback){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState==4) {
            try {
                if (xhr.status==200) {
                    callback(objects);
                }
            } 
            catch(e) {
                alert('Error: ' + e.name);
            }
        }
    };
    
    console.log(url);
    xhr.open("POST", "http://"+url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send(JSON.stringify(objects));
    
}


function sendFriendRequestCallback(objects){
    var btn = document.getElementById("btn-befriend");
    btn.style.display = "none";

    var new_btn = document.getElementById("btn-unfriend");
    new_btn.style.display = "block";
}

function sendUnFriendRequestCallback(objects){
    var btn = document.getElementById("btn-unfriend");
    btn.style.display = "none";
    var new_btn = document.getElementById("btn-befriend");
    new_btn.style.display = "block";
}


function sendFriendRequest(init, recv){
    users = {"init": init, "recv": recv};
    sendJSONHTTPPost(recv.host+"/friendrequest/", users, sendFriendRequestCallback)
}

function sendUnFriendRequest(init, recv){
    users = {"init": init, "recv": recv};
    sendJSONHTTPPost(recv.host+"/unfriendrequest/", users, sendUnFriendRequestCallback)
}
