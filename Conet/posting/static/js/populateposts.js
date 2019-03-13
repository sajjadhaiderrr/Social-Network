window.onload = function() {
    var dataresponse;
    const csrf_token = "{{ csrf_token }}";
    let url = window.location.href.split("/")
    url = url[0] + "//" + url[2] ;
    console.log(url)
    fetch(url + "/posts/api/", {
        method:             "GET",
        mode:               "cors",
        cache:              "no-cache",
        credentials:        "same-origin",
        headers: {
                            "Content-Type": "application/json",
                            "x-csrftoken": csrf_token
        }
      })
      .then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
              response.status);
            return;
          }
          // Examine the text in the response
          response.json().then(function(data) {
            console.log(data);
            var body = document.body
            for(let datas of data){
                var post_info = document.createElement('p');
                for(let attr in datas) {
                    console.log(datas)
                    post_info.innerHTML += attr + ": "+ datas[attr] + "<br>"
                }
                body.appendChild(post_info);
            }
          });
        }
      )
}


