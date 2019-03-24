function fetchGetRequest(url){
    return fetch(url, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "x-csrftoken": csrf_token,
            "Accept": "application/json"
        }
    });
}

function fetchPostRequest(url, sendObjcet){
    return fetch(url, {
        method: "POST",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            "x-csrftoken": csrf_token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(sendObjcet),
    }).then(res=>{
        if (res.status == 200)
            fetchGetRequest('/notification')
            .then(res=>window.location.reload(true));
        else
            return res.json();
    }).then(data=>alert(data['message']));
}

function getFriendRequests() {
    fetchGetRequest("/friendrequest");
}

function acceptRequest(author, friend){
    var send_query = {'query': 'friendrequest',
                    'author': author,
                    'friend': friend}
    fetchPostRequest('/friendrequest', send_query);
}

function declineRequest(author, friend){
    var send_query = {
        'query': 'unfriendrequest',
        'author': author,
        'friend': friend
    }
    fetchPostRequest('/unfriendrequest', send_query);
}