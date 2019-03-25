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
    url + "/posts/" + url[5] + "/comments"
    console.log("url", url);
    console.log(commentForm);
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
          alert("Success");
        }
        else
        {
            alert(response.status);
        }
    });
}
