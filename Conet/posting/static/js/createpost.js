//https://stackoverflow.com/questions/22087076/how-to-make-a-simple-image-upload-using-javascript-html
var encoded_img="";

function test() {
  alert("test");
}

function createPost() {
  let form = {
    title: "",
    description: "",
    categories: "",
    contentType: "",
    content: "",
    visibility: "",
    unlisted: "",
    visibleTo: ""
  }

  form.title = document.getElementById("title").value;
  form.description = document.getElementById("description").value;
  form.categories = document.getElementById("categories").value;

  form.contentType = document.getElementById("contentType").value;
  if (form.contentType == "image/png;base64" || form.contentType == "image/jpeg'base64") {
    form.content = encoded_img;
  }

  form.content = document.getElementById("content").value;
  form.visibility = document.getElementById("visibility").value;

  var radios = document.getElementsByName("unlisted");
  var length = radios.length
  for (var i = 0; i < length; i++) {
    if (radios[i].checked) {
      if (radios[i].value == "Yes") {
        form.unlisted = true;
      }
      else {
        form.unlisted = false;
      }
      break;
    }
  }

  let body = JSON.stringify(form);
  let url = window.location.href.split("/")
  url = url[0] + "//" + url[2] ;
  console.log(body);
  console.log(url)
  return fetch(url + "/posts/", {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    body: body,
    headers: {
      "Content-Type": "application/json",
      "x-csrftoken": csrf_token
    }
  })
  .then (response => {
    if (response.status == 200) {
      alert("Success")
      let url = window.location.href.split("/");
      url = url[0] + "//" + url[2];
      window.location = url + "/posts/view";
    }
    else {
      alert("Error: " + response.status);
    }
  });
}
