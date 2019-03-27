function addComment(post_url, id){
    console.log(id)
    let commentForm = {
          "comment":"",
          "contentType":"text/plain"
    }

    commentForm.comment = document.getElementById(id).value;
    let body = JSON.stringify(commentForm);
    url = post_url + "/comments"
    console.log(url)
    return fetch(url , {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        body: body,
        headers: {
            "Content-Type": 'application/json',
            "Accept": 'application/json',
            "x-csrftoken": csrf_token
        },
        redirect: "follow",
        referrer: "no-referrer",
    })
    .then(response => {
        if (response.status === 200)
        {
          let url = window.location.href;
          window.location = url;
        }
        else
        {
            alert(response.status);
        }
    });
}
// function to send JSON Http post request
function sendJSONHTTPPost(url, objects, callback, remote={}) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            try {
                callback(xhr.response);
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
    
    if (Object.keys(remote).length === 0 && remote.constructor === Object){
        xhr.setRequestHeader("x-csrftoken", csrf_token);
    }else{
        xhr.setRequestHeader("Authentication", "Basic "+ Base64.encode(remote.username + ":" + remote.password));
    }
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

function create_card_showing_friends(friend){
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
    link.href = friend.url+"/";
    link.innerText = "View more";
    button_div.appendChild(link);

    card_body.appendChild(row);
    row_div.appendChild(card_body);
    row_div.appendChild(button_div);
    friend_card.appendChild(row_div);

    return friend_card;
}


// create a list of cards shows the friends
function sendFriendsCallback(response) {
    response = JSON.parse(response);
    friends = response.friends;
    for (var i of friends) {
        var friend = JSON.parse(i);
        var friend_card = create_card_showing_friends(friend);
        document.getElementById('friend-div').appendChild(friend_card);
    }
}

// create a list of cards shows the friends
function sendFollowingFollwerCallback(response) {

    response = JSON.parse(response);
    friends = response.authors;
    for (var i of friends) {
        var friend = i;
        var friend_card = create_card_showing_friends(friend);
        document.getElementById('friend-div').appendChild(friend_card);
    }
}

// function to get a list of friends of current user.
function getFriends(user) {
    url = user
    request_body = {};
    sendJSONHTTPGet(url, request_body, sendFriendsCallback);
}

function getFollowers(user) {
    url = user+"/follower";
    request_body = {};
    sendJSONHTTPGet(url, request_body, sendFollowingFollwerCallback);
}

function getFollowing(user) {
    url = user+"/following";
    request_body = {};
    sendJSONHTTPGet(url, request_body, sendFollowingFollwerCallback);
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

    document.getElementById("profile-card").removeChild(editBtn);
    document.getElementById("profile-card").appendChild(cancelBtn);
    document.getElementById("profile-card").appendChild(comfirmBtn);
}

function setMultiAttributes(obj, attributes){
    for (attr in attributes){
        obj.setAttribute(attr, attributes[attr]);
    }
}

/*
#     #
#     #  ####  #    # ######    #####    ##    ####  ######
#     # #    # ##  ## #         #    #  #  #  #    # #
####### #    # # ## # #####     #    # #    # #      #####
#     # #    # #    # #         #####  ###### #  ### #
#     # #    # #    # #         #      #    # #    # #
#     #  ####  #    # ######    #      #    #  ####  ######

*/
// set # of friends on home page to its # of friends
function get_num_friend_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = user_be_viewed.url + '/friends/';
    document.getElementById("num-friends").appendChild(aTag);
}

function get_num_follower_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = user_be_viewed.url + '/followers/';
    document.getElementById("num-follower").appendChild(aTag);
}

function get_num_following_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = user_be_viewed.url + '/following/';
    document.getElementById("num-following").appendChild(aTag);
}

function get_num_posts_made_callback(response){
    var response = JSON.parse(response);
    var num_posts_made = response.posts.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_posts_made;
    aTag.href = user_be_viewed.url + '/info/';
    document.getElementById("num-posts").appendChild(aTag);
}

// loading and creating cards of post cards
function get_visible_post_callback(response){
    var response = JSON.parse(response);
    if(response.next == "None" && response.posts==[]){
        console.log("The end");
    }else{
        
        for(post of response.posts){
            var card = document.createElement("div");
            card.classList.add("card","home-page-post-card");

            var card_body = document.createElement("div");
            card_body.classList.add("card-body");

            var card_title = document.createElement("a");
            card_title.classList.add("card-title");
            card_title.href = '/posts/' + post.postid + "/";
            var link_to_post_page = document.createElement("h3");
            link_to_post_page.innerText = post.title;
            card_title.appendChild(link_to_post_page);

            /* modify for remote */
            var author_name = document.createElement("a")
            author_name.classList.add("font-weight-light", "text-muted");
            author_name.innerText = post.postauthor.displayName;
            author_name.href= post.postauthor.url+"/";

            var publish_time = document.createElement("a");
            publish_time.classList.add("font-weight-light", "text-muted");
            var publish_date_time = Date.parse(post.published);
            var now = new Date();
            var sec_ago = (now - publish_date_time)/1000;
            var min_ago = sec_ago / 60;
            var hr_ago = min_ago / 60;
            var days_ago = hr_ago / 24;
            if (min_ago < 60){
                publish_time.innerText = Math.round(min_ago) + " mins. ago";
            }else if (hr_ago < 60){
                publish_time.innerText = Math.round(hr_ago) + " hrs. ago";
            }else{
                publish_time.innerText = Math.round(days_ago) + " days ago";
            }
            publish_time.href = '/posts/' + post.postid + "/";

            if (post.contentType=="text/plain") {
              var content = document.createElement("p");
              content.innerText = post.content;
            }else if(post.contentType=="text/markdown"){
                var converter = new showdown.Converter();
                var md = post.content;
                var html = converter.makeHtml(md);
                var content = document.createElement("div");
                content.innerHTML = html;
            }else {
              var content = document.createElement("img");
              content.setAttribute("src", post.content);
              content.setAttribute("width", "100%");
              content.setAttribute("height", "auto");
            }
            
            var hr = document.createElement("hr");

            var commentbox = document.createElement("div");
            commentbox.classList.add("input-group", "shadow-textarea");
            var comment_textarea = document.createElement("textarea");
            comment_textarea.classList.add('form-control','z-depth-1');
            comment_textarea.id = "addcommenttext"+num_post_counter;
            comment_textarea.setAttribute("rows", "1");
            comment_textarea.setAttribute("placeholder", "Comment...");
            comment_textarea.setAttribute("style", "resize:none");
            
            var comment_btn = document.createElement("span");
            comment_btn.classList.add("btn", "btn-primary");
            comment_btn.id = "addcommentbutton"+num_post_counter;
            // if user is logged in, give him permision to add comment
            if(current_user.id != "None"){
                comment_btn.setAttribute("onClick","addComment('" + post.origin+ "','"+comment_textarea.id+"');");
            }else{
                // else: redirect to login page
                comment_btn.onclick = function(){window.location.replace(post.postauthor.host);}
            }
            comment_btn.innerText = "Send";
            commentbox.appendChild(comment_textarea);
            commentbox.appendChild(comment_btn);

            card_body.appendChild(card_title);
            card_body.appendChild(author_name);
            card_body.appendChild(document.createElement("br"));
            card_body.appendChild(publish_time);
            card_body.appendChild(document.createElement("hr"));
            card_body.appendChild(content);
            card_body.appendChild(hr);
            card_body.appendChild(commentbox);
            card.appendChild(card_body);
            document.getElementById("home_page_post_cards").appendChild(card);
            num_post_counter += 1;
        }
    }
}

// function for initializing home page
function init_home_page(user){
    num_post_counter = 0;
    page_number = 0;
    current_user = user;
    var request_body = {};
    var friend_url = user.url + "/friends";
    var made_posts_url = user.url+"/madeposts";
    var follower_url = user.url+"/follower";
    var following_url = user.url + "/following";
    var fetch_posts_url = user.host + "/author/posts" + "?page="+page_number;
    sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback);
    sendJSONHTTPGet(made_posts_url, request_body, get_num_posts_made_callback);
    sendJSONHTTPGet(follower_url, request_body, get_num_follower_callback);
    sendJSONHTTPGet(following_url, request_body, get_num_following_callback);
    sendJSONHTTPGet(fetch_posts_url, request_body, get_visible_post_callback);
}

/*
 ###
  #  #    # ######  ####     #####    ##    ####  ######
  #  ##   # #      #    #    #    #  #  #  #    # #
  #  # #  # #####  #    #    #    # #    # #      #####
  #  #  # # #      #    #    #####  ###### #  ### #
  #  #   ## #      #    #    #      #    # #    # #
 ### #    # #       ####     #      #    #  ####  ######
*/

// callback function after sending init
// - Simply change the button to "unfriend" if they are friends
function sendInitInfoRequestCallback(response) {
    var response = JSON.parse(response);
    var following = false;
    for(var relation of response.authors){
        if(relation.id == user_be_viewed.id){
            following = true;
            break;
        }
    }
    if (!following) {
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

function get_profile_callback(response){
    var response = JSON.parse(response);

    // adding first name
    var fn = document.createElement("p");
    fn.classList.add("text-secondary", "profile-card-content");
    fn.innerText = response.first_name;
    fn.setAttribute("id", "first_name");
    document.getElementById("profile-card-info").appendChild(fn);

    // adding last name
    var ln = document.createElement("p");
    ln.classList.add("text-secondary", "profile-card-content");
    ln.innerText = response.last_name;
    ln.setAttribute("id", "last_name");
    document.getElementById("profile-card-info").appendChild(ln);

    // adding bio
    var bio = document.createElement("p");
    bio.classList.add("text-secondary", "profile-card-content");
    if (response.bio == ""){
        response.bio = "None";
    }
    bio.innerText = response.bio;
    bio.setAttribute("id", "bio");
    document.getElementById("profile-card-info").appendChild(bio);

    // add email
    var email = document.createElement("a");
    email.classList.add("text-secondary", "profile-card-content")
    var email_icon = document.createElement("span");
    email_icon.classList.add("oi", "oi-envelope-closed");
    email.appendChild(email_icon);
    email.innerHTML += "  " + response.email;
    email.href = "mailto:"+response.email;
    email.setAttribute("id", "email");
    document.getElementById("profile-card-info").appendChild(email);
    var br = document.createElement("br");
    document.getElementById("profile-card-info").appendChild(br);


    // add github
    var github = document.createElement("a");
    github.classList.add("text-secondary", "profile-card-content")
    var github_icon = document.createElement("span");
    github_icon.classList.add("oi", "oi-fork");
    github.appendChild(github_icon);
    github.innerHTML += " " + response.github;
    github.href = response.github;
    github.setAttribute("id", "github");
    document.getElementById("profile-card-info").appendChild(github);
    var br = document.createElement("br");
    document.getElementById("profile-card-info").appendChild(br);

    // add host
    var host = document.createElement("a");
    host.classList.add("text-secondary", "profile-card-content")
    var host_icon = document.createElement("span");
    host_icon.classList.add("oi", "oi-flag");
    host.appendChild(host_icon);
    host.innerHTML += " " + response.host;
    host.href = response.host;
    document.getElementById("profile-card-info").appendChild(host);
    var br = document.createElement("br");
    document.getElementById("profile-card-info").appendChild(br);
}


function init_info_page(init, recv_url, remote, from_one_host) {
    num_post_counter = 0;
    current_user = init;
    var request_body = {};
    var profile_url = recv_url;
    var friend_url = recv_url + "/friends";
    var posts_url = recv_url+"/posts";
    
    // for author from one host, display follower and followings
    if(from_one_host){
        var follower_url = recv_url +"/follower";
        var following_url = recv_url + "/following";
        sendJSONHTTPGet(profile_url, {}, get_profile_callback);
        sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback);
        sendJSONHTTPGet(posts_url, request_body, get_num_posts_made_callback);
        sendJSONHTTPGet(follower_url, request_body, get_num_follower_callback);
        sendJSONHTTPGet(following_url, request_body, get_num_following_callback);
    }else{
        // for author from another host, only shows friends and posts.
        sendJSONHTTPGet(profile_url, {}, get_profile_callback, remote);
        sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback, remote);
        sendJSONHTTPGet(posts_url, request_body, get_num_posts_made_callback, remote);
    }

    // loading follow and unfollow btn
    if(init.id != recv.id && init.id!="None"){
        sendJSONHTTPGet(init.host + "/author/" + init.id + "/following", request_body, sendInitInfoRequestCallback);
    }
    sendJSONHTTPGet(made_posts_url, request_body, get_visible_post_callback);
}
