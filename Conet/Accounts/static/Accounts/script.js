function sendJSONHTTPPost(url, objects, callback){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState==4) {
            try {
                if (xhr.status==200) {
                    callback(JSON.parse(xhr.responseText));
                }
            } 
            catch(e) {
                alert('Error: ' + e.name);
            }
        }
    };

    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send(JSON.stringify(objects));
}