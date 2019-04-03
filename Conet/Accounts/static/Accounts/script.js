
// function to send JSON Http post request
function sendJSONHTTPPost(url, objects, callback, remote={}) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            try {
                callback(xhr.response);
            }
            catch (e) {
                //alert('XHR Error: ' + e.name);
                console.log(url);
            }
        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");

    //if (Object.keys(remote).length === 0 && remote.constructor === Object){
    xhr.setRequestHeader("x-csrftoken", csrf_token);
    //}else{
    //    xhr.setRequestHeader("Authorization", "Basic "+ Base64.encode(remote.username + ":" + remote.password));
    //}
    xhr.send(JSON.stringify(objects));
}

function sendJSONHTTPGet(url, objects, callback, remote={}) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                callback(xhr.response);
            }
            
        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("GET", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    if (Object.keys(remote).length === 0 && remote.constructor === Object) {
        xhr.setRequestHeader("x-csrftoken", csrf_token);
    } else {
        xhr.setRequestHeader("Authorization", "Basic " + btoa(remote.username + ":" + remote.password));
    }
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

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function addComment(post_url, id, same_host){
    // Reference: https://stackoverflow.com/questions/736513/how-do-i-parse-a-url-into-hostname-and-path-in-javascript
    var getLocation = function(href) {
        var l = document.createElement("a");
        l.href = href;
        return l;
    };

    var header = {"Content-Type": 'application/json',
                  "Accept": 'application/json',
                  "x-request-user-id": request_user_id};
    if (same_host){
        header['x-csrftoken'] = csrf_token;
    }else{
        for (r of remote){
            post_host = getLocation(post_url).host;
            remote_host = getLocation(r.host).host;
            console.log(post_host == remote_host)
            console.log(post_url);
            console.log(remote_host);
            console.log(r.host);
            if (remote_host == post_host){
                header["Authorization"] = "Basic " + btoa(r.username + ":" + r.password);
            }
        } 
    };
    let commentForm = {
        "query":"addComment",
        "post": post_url,
        "comment":{"author":{"id":current_user.id,
                             "host": current_user.host,
                             "displayName": current_user.displayName,
                             "url": current_user.url,
                             "github": current_user.github
                    },
                   "comment":"",
                   "contentType":"text/plain",
                   "published": new Date().toISOString(),
                   "id": uuidv4()    
        }
    };

    commentForm.comment.comment = document.getElementById(id).value;
    console.log(commentForm);
    let body = JSON.stringify(commentForm);
    url = post_url + "/comments"
    return fetch(url , {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        body: body,
        headers: header,

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
        }
    });
    
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
    sendJSONHTTPPost(init.host + "/friendrequest", users, sendFriendRequestCallback);
}

// function to send unfriend request
function sendUnFriendRequest(init, recv) {
    users = { "query": "unfriendrequest", "author": init, "friend": recv };
    sendJSONHTTPPost(init.host + "/unfriendrequest", users, sendUnFriendRequestCallback);
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
    link.href = "http://"+window.location.hostname+":"+window.location.port+"/author/"+friend.id+"/info/?host="+friend.host;
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

        //var friend = JSON.parse(i);
        var friend_card = create_card_showing_friends(i);
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
    aTag.href = "http://"+ window.location.host+"/author/"+user_be_viewed.id+'/friends/';
    document.getElementById("num-friends").appendChild(aTag);
}

function get_num_follower_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = "http://"+ window.location.host+"/author/"+user_be_viewed.id + '/followers/';
    document.getElementById("num-follower").appendChild(aTag);
}

function get_num_following_callback(response){
    var response = JSON.parse(response);
    var num_friends = response.authors.length;
    var aTag = document.createElement("a");
    aTag.innerText=num_friends;
    aTag.href = "http://"+ window.location.host+"/author/"+user_be_viewed.id+ '/following/';
    document.getElementById("num-following").appendChild(aTag);
}

function get_num_posts_made_callback(response){
    var response = JSON.parse(response);
    var num_posts_made = response.count;
    var aTag = document.createElement("a");
    aTag.innerText=num_posts_made;
    aTag.href = "http://"+ window.location.host+"/author/"+user_be_viewed.id + '/info/?host=' + user_be_viewed.host;
    document.getElementById("num-posts").appendChild(aTag);
}
function deletePost(post) {
  let url = post.origin;
  return fetch(url, {
    method: "DELETE",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
        "x-csrftoken": csrf_token
    },
    redirect: "follow",
    referrer: "no-referrer",
})
.then(response => {
  if (response.status === 204)  {
    window.location.reload(true);
  }
  else
  {
    alert(response.status);
  }
});
}

function editPost(post, divElem) {
  console.log(window.location.origin+'/posts/'+'edit/'+post.postid+'/');
  window.location.href = window.location.origin+'/posts/'+'edit/'+post.postid+'/';
}


// Reference: https://stackoverflow.com/questions/6048561/setting-onclick-to-use-current-value-of-variable-in-loop
var deletePostHandler = function(arg) {
  return function() { deletePost(arg); };
}
var editPostHandler = function(arg, arg1) {
  return function() { editPost(arg, arg1); };
}
// loading and creating cards of post cards
function get_visible_post_callback(response){
    var response = JSON.parse(response);
    console.log(response);
    if(false&&(response.next == "None" && response.posts==[])){
        console.log("The end");
    }else{
        var i=0;
        for(post of response.posts){

            var card = document.createElement("div");
            card.classList.add("card","home-page-post-card");

            // Card menu for delete
            var card_menu = document.createElement("a");
            card_menu.href="#";
            card_menu.innerHTML = '<i class="material-icons">delete</i>';
            card_menu.style.color = '#007bff';
            card_menu.style.position = "absolute";
            card_menu.style.right="15px";
            //card_menu.addEventListener("click", function () {("click",function(){deletePost(post)}));
            card_menu.onclick = deletePostHandler(post);

            var card_edit = document.createElement("a");
            card_edit.href="#";
            card_edit.innerHTML = '<i class="material-icons">edit</i>';
            card_edit.style.color = '#007bff';
            card_edit.style.position = "absolute";
            card_edit.style.right="45px";
            //card_menu.addEventListener("click", function () {("click",function(){deletePost(post)}));
            card_edit.onclick = editPostHandler(post, card_edit);


            var card_body = document.createElement("div");
            card_body.classList.add("card-body");

            var card_title = document.createElement("a");
            card_title.classList.add("card-title");
            card_title.href = '/posts/' + post.postid + "/?host=" + post.author.host;
            var link_to_post_page = document.createElement("h3");
            link_to_post_page.innerText = post.title;
            card_title.appendChild(link_to_post_page);

            /* modify for remote */
            var author_name = document.createElement("a")
            author_name.classList.add("font-weight-light", "text-muted");
            author_name.innerText = post.author.displayName;
            author_name.href = "http://"+ window.location.hostname+":"+window.location.port+"/author/"+post.author.id+"/info/?host=" + post.author.host;
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
            } else if(post.contentType=="image/png;base64" || post.contentType=="image/jpeg;base64" ){
              var content = document.createElement("img");
              content.setAttribute("src", post.content);
              content.setAttribute("width", "100%");
              content.setAttribute("height", "auto");
            }else if(post.contentType=="application/base64"){
              var content = document.createElement("a");
              content.setAttribute('href',post.content);
              content.innerText = "View "+post.title+" in new tab (if application is supported by your browser) or Download (Right click -> Save As)";
              content.click()
            }

            var hr = document.createElement("hr");

            // for comment box and comment btn
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
                var same_host = true;
                if (post.author.host != current_user.host){
                    var same_host = false;
                }
                comment_btn.setAttribute("onClick","addComment('" + post.origin+ "','"+comment_textarea.id +"',"+same_host +");");
            }else{
                // else: redirect to login page
                comment_btn.onclick = function(){window.location.replace(post.author.host);}
            }
            comment_btn.innerText = "Send";
            commentbox.appendChild(comment_textarea);
            commentbox.appendChild(comment_btn);

            // for displaying comments
            var comments_div = document.createElement("div");

            for(comment of post.comments){
                var comment_title = document.createElement("div");
                console.log(comment);
                var comment_author_name = document.createElement("a");
                comment_author_name.href = "http://"+ window.location.hostname+":"+window.location.port+"/author/"+comment.author.id+"/info/?host=" + comment.author.host;
                comment_author_name.innerText = comment.author.displayName;
                comment_author_name.classList.add("float-sm-left", "font-weight-bold",'text-secondary');
                comment_author_name.setAttribute("style","font-size:10pt; margin-top:-10pt;");

                var comment_published = document.createElement("a");
                comment_published.classList.add("font-weight-light", "text-muted");
                comment_published.classList.add("float-sm-left",'text-secondary');
                comment_published.setAttribute("style","font-size:10pt; margin-top:-10pt; margin-left:5pt;");
                var publish_date_time = Date.parse(comment.published);
                var now = new Date();
                var sec_ago = (now - publish_date_time)/1000;
                var min_ago = sec_ago / 60;
                var hr_ago = min_ago / 60;
                var days_ago = hr_ago / 24;
                if (min_ago < 60){
                    comment_published.innerText = Math.round(min_ago) + " mins. ago";
                }else if (hr_ago < 60){
                    comment_published.innerText = Math.round(hr_ago) + " hrs. ago";
                }else{
                    comment_published.innerText = Math.round(days_ago) + " days ago";
                }

                var comment_content = document.createElement("p");
                comment_content.innerText = comment.comment;
                comment_content.setAttribute("style","font-size:10pt; margin-top:-10pt;");

                comment_title.appendChild(comment_author_name);
                comment_title.append(comment_published);
                comments_div.appendChild(comment_title);
                comments_div.appendChild(document.createElement("br"));
                comments_div.append(comment_content);

                comments_div.appendChild(document.createElement("hr"));
            }

            card_body.appendChild(card_title);
            // Add edit/delete menu if author
            if (current_user.id == post.author.id) {
              card_body.appendChild(card_edit);
              card_body.appendChild(card_menu);
            }
            card_body.appendChild(author_name);
            card_body.appendChild(document.createElement("br"));
            card_body.appendChild(publish_time);
            card_body.appendChild(document.createElement("hr"));
            card_body.appendChild(content);

            card_body.appendChild(commentbox);
            card_body.appendChild(document.createElement("hr"));
            card_body.appendChild(comments_div);
            card.appendChild(card_body);
            document.getElementById("home_page_post_cards").appendChild(card);
            num_post_counter += 1;
        }
    }
}

// loading and creating cards of post cards
function fetch_github_stream_callback(response){
    var response = JSON.parse(response);
    for(post of response){
        //console.log(post);
        var card = document.createElement("div");
        card.classList.add("card","home-page-post-card");

        var card_body = document.createElement("div");
        card_body.classList.add("card-body");

        var card_title = document.createElement("a");
        card_title.classList.add("card-title");
        card_title.href = '/posts/' + post.postid + "/?host=" + post.author.host ;
        var link_to_post_page = document.createElement("h3");
        link_to_post_page.innerText = "Github Post";
        card_title.appendChild(link_to_post_page);

        var publish_time = document.createElement("a");
        publish_time.classList.add("font-weight-light", "text-muted");
        publish_time.innerText = post.date;

        var content = document.createElement("p");
        content.innerText = post.event_message;

        card_body.appendChild(card_title);
        card_body.appendChild(publish_time);
        card_body.appendChild(document.createElement("hr"));
        card_body.appendChild(content);
        card.appendChild(card_body);
        document.getElementById("home_page_post_cards").appendChild(card);
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
    var fetch_posts_url = user.host + "/author/posts";
    var fetch_github_stream_url = user.host + "/posts/view/github";
    sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback);
    sendJSONHTTPGet(made_posts_url, request_body, get_num_posts_made_callback);
    sendJSONHTTPGet(follower_url, request_body, get_num_follower_callback);
    sendJSONHTTPGet(following_url, request_body, get_num_following_callback);
    sendJSONHTTPGet(fetch_posts_url, request_body, get_visible_post_callback);
    sendJSONHTTPGet(fetch_github_stream_url, request_body, fetch_github_stream_callback);
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
    console.log(response);
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
    // add title
    var displayName = document.getElementById("displayName");
    displayName.innerText = response.displayName;
    user_be_viewed.displayName = response.displayName;
    //
    try{
        document.getElementById("btn-befriend").onclick = function(){sendFriendRequest(current_user, user_be_viewed);};
        document.getElementById("btn-unfriend").onclick = function(){sendUnFriendRequest(current_user, user_be_viewed);};
    }catch{

    }

    //document.getElementById("btn-befriend").setAttribute("onClick","sendFriendRequest(" + current_user+ ","+user_be_viewed+");");
    //document.getElementById("btn-unfriend").setAttribute("onClick","sendUnFriendRequest(" + current_user+ ","+user_be_viewed+");");
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


function init_info_page(init, recv, remote, from_one_host) {
    num_post_counter = 0;
    current_user = init;
    var request_body = {};
    var profile_url = recv.url;
    var friend_url = recv.url + "/friends";
    var posts_url = recv.url+"/posts";
    var github_url = recv.url+"/posts/github";
    // for author from one host, display follower and followings
    if(from_one_host){
        var follower_url = recv.url +"/follower";
        var following_url = recv.url + "/following";
        sendJSONHTTPGet(profile_url, {}, get_profile_callback);
        sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback);
        sendJSONHTTPGet(posts_url, request_body, get_num_posts_made_callback);
        sendJSONHTTPGet(follower_url, request_body, get_num_follower_callback);
        sendJSONHTTPGet(following_url, request_body, get_num_following_callback);
        sendJSONHTTPGet(posts_url, request_body, get_visible_post_callback);
    }else{
        // for author from another host, only shows friends and posts.
        sendJSONHTTPGet(profile_url, {}, get_profile_callback, remote[0]);
        sendJSONHTTPGet(friend_url, request_body, get_num_friend_callback, remote[0]);
        sendJSONHTTPGet(posts_url, request_body, get_num_posts_made_callback, remote[0]);
        sendJSONHTTPGet(posts_url, request_body, get_visible_post_callback, remote[0]);
    }

    // loading follow and unfollow btn
    if(init.id != recv.id && init.id!="None"){
        sendJSONHTTPGet(init.host + "/author/" + init.id + "/following", request_body, sendInitInfoRequestCallback);
    }
    //sendJSONHTTPGet(posts_url, request_body, get_visible_post_callback, remote);
    // sendJSONHTTPGet(github_url, request_body, fetch_github_stream_callback);
}
