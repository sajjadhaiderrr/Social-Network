function fetchGetRequest(url){
    return fetch(url, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            //"x-csrftoken": csrf_token,
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

//first request would be set to 0 sec
//update counts of friendrequest every 10 sec
function setBadgeCounter(counts){
    console.log(counts)
    var badge = document.getElementsByClassName('badge-danger')[0];
    if (counts > 0)
        badge.innerHTML = counts;
    else
        badge.innerHTML = "";
    setTimeout(updateFriendRequestCount, 30000);
}

function updateFriendRequestCount() {
    fetchGetRequest('/friendrequest')
        .then(res=>res.json())
        .then(data=>setBadgeCounter(data['counts']));
}

setTimeout(updateFriendRequestCount, 0);