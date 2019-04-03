function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function addCommentOnSinglePage(post_id, post_url, same_host){
    var header = {"Content-Type": 'application/json',
                  "Accept": 'application/json',
                  "x-request-user-id": request_user_id};
    if (same_host){
        header['x-csrftoken'] = csrf_token;
    }else{
        header["Authorization"] = "Basic " + btoa(remote.username + ":" + remote.password);
    }
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
    }

    commentForm.comment.comment = document.getElementById("addcommenttext").value;
    console.log(commentForm);
    let body = JSON.stringify(commentForm);
    let url = post_url+"/comments"
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
            alert(response.status);
        }
    });
}

// need to be modified for remote functionality
function init_single_post_page(origin, authenticated, request_user_id, same_host,remote={}){
    var url = origin;
    var header = {"Content-Type": 'application/json',
                  "Accept": 'application/json',
                  "x-request-user-id": request_user_id};
    if (same_host){
        header['x-csrftoken'] = csrf_token;
    }else{
        console.log(remote)
        header["Authorization"] = "Basic " + btoa(remote.username + ":" + remote.password);
    }
    return fetch(url , {
        method: "GET",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: header,
        redirect: "follow",
        referrer: "no-referrer"
    }).then(response => {
        if (response.status === 200){
            return response.json();
        }else{
            var status_code = document.createElement("h1");
            status_code.innerText = response.status + ": " + response.statusText;
            document.getElementById("post-content").appendChild(status_code);
        }
    }).then(json =>{
        console.log(json);
        // display title
        document.getElementById("post-title").innerText = json.post.title;

        // display who is author
        document.getElementById("post-author-link").innerText = json.post.author.displayName;
        document.getElementById("post-author-link").href = json.post.author.url + "/";

        // display times
        var publish_date_time = Date.parse(json.post.published);
        var now = new Date();
        var sec_ago = (now - publish_date_time)/1000;
        var min_ago = sec_ago / 60;
        var hr_ago = min_ago / 60;
        var days_ago = hr_ago / 24;
        if (min_ago < 60){
            document.getElementById("published").innerText = Math.round(min_ago) + " mins. ago";
        }else if (hr_ago < 60){
            document.getElementById("published").innerText = Math.round(hr_ago) + " hrs. ago";
        }else{
            document.getElementById("published").innerText = Math.round(days_ago) + " days ago";
        }

        // display content
        if(json.post.contentType == 'text/plain'){
            // display the plain text content
            var content = document.createElement("p");
            content.innerText = json.post.content;
            document.getElementById("post-content").appendChild(content);
        }else if(json.post.contentType=="text/markdown"){
            var converter = new showdown.Converter();
            var md = json.post.content;
            var html = converter.makeHtml(md);
            var content = document.createElement("div");
            content.innerHTML = html;
            document.getElementById("post-content").appendChild(content);
        }else if(json.post.contentType=="image/png;base64" || json.post.contentType=="image/jpeg;base64" ){
            var content = document.createElement("img");
            content.setAttribute("src", json.post.content);
            content.setAttribute("width", "100%");
            content.setAttribute("height", "auto");
            document.getElementById("post-image").appendChild(content);
        }
        else if(json.post.contentType=="application/base64"){
            var content = document.createElement("a");
            content.setAttribute('href',json.post.content);
            content.innerText = "View "+json.post.title+" in new tab (if application is supported by your browser) or Download (Right click -> Save As)";
            content.click()
            document.getElementById("post-image").appendChild(content);
        }



        // display comment box
        var commentbox = document.createElement("div");
        commentbox.classList.add("input-group", "shadow-textarea");
        var comment_textarea = document.createElement("textarea");
        comment_textarea.classList.add('form-control','z-depth-1');
        comment_textarea.id = "addcommenttext";
        comment_textarea.setAttribute("rows", "1");
        comment_textarea.setAttribute("placeholder", "Comment...");
        comment_textarea.setAttribute("style", "resize:none");

        var comment_btn = document.createElement("span");
        comment_btn.classList.add("btn", "btn-primary");
        comment_btn.id = "addcommentbutton";
        if(authenticated == "True"){
            comment_btn.onclick = function(){addCommentOnSinglePage(json.post.postid, json.post.origin, same_host)} ;
        }else{
            comment_btn.onclick = function(){window.location.replace(json.post.author.host);} ;
        }

        comment_btn.innerText = "Send";

        commentbox.appendChild(comment_textarea);
        commentbox.appendChild(comment_btn);
        document.getElementById("create-comment").appendChild(commentbox);
        
        document.getElementById("post-comments").appendChild(document.createElement("hr"))
        for(comment of json.post.comments){
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
            document.getElementById("post-comments").appendChild(comment_title);
            document.getElementById("post-comments").appendChild(document.createElement("br"));
            document.getElementById("post-comments").append(comment_content);
            
            document.getElementById("post-comments").appendChild(document.createElement("hr"));
        }
    });
}
