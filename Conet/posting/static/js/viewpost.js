function getPost(url)
{
    return fetch(url, {
        method: "GET",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json"
        },
        redirect: "follow",
        referrer: "no-referrer",
    })
    .then(response => response.json());
}

function addCommentOnSinglePage(post_id)
{
    let commentForm = {
          "comment":"",
          "contentType":"text/plain"
    }

    commentForm.comment = document.getElementById("addcommenttext").value;
    let body = JSON.stringify(commentForm);
    let url = window.location.href.split("/")
    url = url[0] + "//" + url[2] ;
    url = url + "/posts/"+post_id+"/comments"
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

// need to be modified for remote functionality
function init_single_post_page(origin, authenticated){
    url = origin;
    return fetch(url , {
        method: "GET",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": 'application/json',
            "Accept": 'application/json',
            "x-csrftoken": csrf_token
        },
        redirect: "follow",
        referrer: "no-referrer",

    })
    .then(response => {
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
            comment_btn.onclick = function(){addCommentOnSinglePage(json.post.postid)} ;
        }else{
            comment_btn.onclick = function(){window.location.replace(json.post.author.host);} ;
        }

        comment_btn.innerText = "Send";

        commentbox.appendChild(comment_textarea);
        commentbox.appendChild(comment_btn);
        document.getElementById("create-comment").appendChild(commentbox);
    });
}
