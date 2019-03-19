
// function to send JSON Http post request
function sendJSONHTTPPost(url, objects, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            try {
                if (xhr.status == 200) {
                    callback(xhr.response);
                }
            }
            catch (e) {
                alert('Error: ' + e.name);
            }
        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("x-csrftoken", csrf_token);
    xhr.send(JSON.stringify(objects));
}

function sendJSONHTTPGet(url, objects, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            try {
                if (xhr.status == 200) {
                    callback(xhr.response);
                }
            }
            catch (e) {
                alert('Error: ' + e.name);
            }
        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("GET", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("x-csrftoken", csrf_token);
    xhr.send(JSON.stringify(objects));
}

// callback function after sending friend request
// - Simply change the "befriend" button to "unfriend" button
function sendFriendRequestCallback(objects) {
    var btn = document.getElementById("btn-befriend");
    btn.style.display = "none";

    var new_btn = document.getElementById("btn-unfriend");
    new_btn.style.display = "block";
}

// callback function after sending unfriend request
// - Simply change the "unfriend" button to "befriend" button
function sendUnFriendRequestCallback(objects) {
    var btn = document.getElementById("btn-unfriend");
    btn.style.display = "none";
    var new_btn = document.getElementById("btn-befriend");
    new_btn.style.display = "block";
}

// function to send befriend request
function sendFriendRequest(init, recv) {
    users = { "query": "friendrequest", "author": init, "friend": recv };
    sendJSONHTTPPost(recv.host + "/friendrequest", users, sendFriendRequestCallback);
}

// function to send unfriend request
function sendUnFriendRequest(init, recv) {
    users = { "query": "unfriendrequest", "author": init, "friend": recv };
    sendJSONHTTPPost(recv.host + "/unfriendrequest", users, sendUnFriendRequestCallback);
}

// callback function after sending init
// - Simply change the button to "unfriend" if they are friends
function sendInitInfoRequestCallback(response) {
    var response = JSON.parse(response);
    if (response.authors.length == 0) {
        var btn = document.getElementById("btn-unfriend");
        btn.style.display = "none";
        var new_btn = document.getElementById("btn-befriend");
        new_btn.style.display = "block";
    } else {
        var btn = document.getElementById("btn-befriend");
        btn.style.display = "none";
        var new_btn = document.getElementById("btn-unfriend");
        new_btn.style.display = "block";
    }
}

function init_info_page(init, recv) {
    console.log("initing")
    var request_body = { 'authors': "['" + recv.id + "']" };
    sendJSONHTTPGet(init.host + "/author/" + init.id + "/following", request_body, sendInitInfoRequestCallback);
}

function sendLoadUserProfileCallback(response) {
    var response = JSON.parse(response);
    for (var key in response) {
        var inner_div = document.createElement("div");
        inner_div.classList.add("row");
        var inner_title = document.createElement("dt");
        inner_title.classList.add("col-sm-3");
        inner_title.innerText = key;

        var inner_text = document.createElement("dd");
        inner_text.classList.add("col-sm-9");
        inner_text.innerText = response[key];
        inner_text.setAttribute("id", key);

        inner_div.appendChild(inner_title);
        inner_div.appendChild(inner_text);

        document.getElementById("profile-outer-div").appendChild(inner_div);
    }
}

// function to search other users
function load_user_profile(current_user, user_be_viewed) {
    var request_body = { 'authors': "['" + user_be_viewed.id + "']" };
    sendJSONHTTPGet(current_user.host + "/author/" + user_be_viewed.id, request_body, sendLoadUserProfileCallback);
}

// create a list of cards shows the friends
function sendFriendsCallback(response) {
    response = JSON.parse(response);
    friends = response.friends;
    for (var i of friends) {
        var friend = JSON.parse(i);

        var friend_card = document.createElement("div");
        friend_card.classList.add("card", "search-results");

        var row_div = document.createElement("div");
        row_div.classList.add("row");

        var card_body = document.createElement("div");
        card_body.classList.add("card-body", "col-sm-8");

        var card_title = document.createElement("h3");
        card_title.innerText = friend.displayName;
        card_body.appendChild(card_title);

        var row = document.createElement("dl");
        row.classList.add("row");

        var bio_title = document.createElement("dt");
        bio_title.classList.add("col-sm-3");
        bio_title.innerText = "Biography";
        var bio_dd = document.createElement("dd");
        bio_dd.classList.add("col-sm-9");
        bio_dd.innerText = friend.bio;
        row.appendChild(bio_title);
        row.appendChild(bio_dd);


        var host_title = document.createElement("dt");
        host_title.classList.add("col-sm-3");
        host_title.innerText = "Host";
        var host_dd = document.createElement("dd");
        host_dd.classList.add("col-sm-9");
        var link = document.createElement("a");
        link.href = friend.host;
        link.innerText = friend.host;
        host_dd.appendChild(link);
        row.appendChild(host_title);
        row.appendChild(host_dd);

        var git_title = document.createElement("dt");
        git_title.classList.add("col-sm-3");
        git_title.innerText = "Github";
        var git_dd = document.createElement("dd");
        git_dd.classList.add("col-sm-9");
        var link = document.createElement("a");
        link.href = friend.github;
        link.innerText = friend.github;
        git_dd.appendChild(link);
        row.appendChild(git_title);
        row.appendChild(git_dd);

        var button_div = document.createElement("div");
        button_div.classList.add("card-body", "col-sm-2");
        var link = document.createElement("a");
        link.classList.add("btn", "btn-primary", "align-middle")
        link.href = friend.url;
        link.innerText = "View more";
        button_div.appendChild(link);

        card_body.appendChild(row);
        row_div.appendChild(card_body);
        row_div.appendChild(button_div);
        friend_card.appendChild(row_div);

        document.getElementById('friend-div').appendChild(friend_card);
    }
}

// function to get a list of friends of current user.
function getFriends(user) {
    url = user.slice(0, -1);
    request_body = {};
    sendJSONHTTPGet(url, request_body, sendFriendsCallback);
}

function backToProfile(recoverList) {
}

//referenec: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
function fetchPutRequest(url, profileInfo) {
    return fetch(url, {
        method: "PUT",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "x-csrftoken": csrf_token,
        },
        body: JSON.stringify(profileInfo),
    }).then(res => {
        console.log(res);
        if(res.status == 400)
            console.log("input data is invalid");
        else
            window.location.reload(true);
        });
}

//
function editProfile() {
    var intendToEdit = document.querySelectorAll("#email, #bio, #first_name, #last_name, #displayName, #github");
    var editBtn = document.getElementById("btn-edit");
    var comfirmBtn = document.createElement("button");
    var cancelBtn = document.createElement("button");
    var data = {};
    var btnAttrs;

    comfirmBtn.innerText = "Comfirm";
    btnAttrs = {"class": "btn btn-primary", "id": "btn-comfirm"};
    setMultiAttributes(comfirmBtn, btnAttrs);
    cancelBtn.innerText = "Cancel";
    btnAttrs = {"class": "btn btn-primary", "id": "btn-cancel"};
    setMultiAttributes(cancelBtn, btnAttrs);


    for (var idx = 0; idx < intendToEdit.length; idx++) {
        var input_field = document.createElement("input");

        input_field.setAttribute("type", "text");
        input_field.setAttribute("name", intendToEdit[idx].id);
        input_field.value = intendToEdit[idx].innerText;
        data[input_field.name] = input_field;
        intendToEdit[idx].parentNode.replaceChild(input_field, intendToEdit[idx]);
    }

    comfirmBtn.addEventListener("click", function () {
        fetchPutRequest(window.location.href, {
            'email': data['email'].value, 
            'bio': data['bio'].value,
            'first_name': data['first_name'].value,
            'last_name': data['last_name'].value,
            'displayName': data['displayName'].value,
            'github': data['github'].value
        })
    });

    cancelBtn.addEventListener("click", backToProfile());

    document.getElementsByClassName("content")[0].removeChild(editBtn);
    document.getElementsByClassName("content")[0].appendChild(cancelBtn);
    document.getElementsByClassName("content")[0].appendChild(comfirmBtn);
}

function setMultiAttributes(obj, attributes){
    for (attr in attributes){
        console.log(attr);
        obj.setAttribute(attr, attributes[attr]);
    }
}

// set # of friends on home page to its # of friends
function get_num_friend_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = 'friends/';
    document.getElementById("num-friends").appendChild(aTag);
}

function get_num_posts_made_callback(response){
    var response = JSON.parse(response);
    var num_posts_made = response.posts.length;
    document.getElementById("num-posts").innerText = num_posts_made;
}

// function for initializing home page
function init_home_page(user){
    var request_body = {};
    var friend_url = user.url + "friends"
    var made_posts_url = user.url+"madeposts"
    sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback);
    sendJSONHTTPGet(made_posts_url, request_body, get_num_posts_made_callback);
}