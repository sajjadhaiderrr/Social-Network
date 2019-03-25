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

function addComment(post_id)
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


function init_single_post_page(origin){
    console.log(origin);
    url = origin;
    return fetch(url , {
        method: "GET",
        /*
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
        */
    })
    .then(response => {
        if (response.status === 200){
            return response.json();
        }else{
            alert(response.status);
        }
    }).then(json =>{
        console.log(json);

        // display title
        document.getElementById("post-title").innerText = json.post.title;
        
        // display who is author
        document.getElementById("post-author-link").innerText = json.post.postauthor.displayName;
        document.getElementById("post-author-link").href = json.post.postauthor.url + "/";
        
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
        }

        // display comment
        
    });
} 
