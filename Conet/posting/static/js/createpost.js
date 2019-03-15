//https://stackoverflow.com/questions/22087076/how-to-make-a-simple-image-upload-using-javascript-html
var uploadedImage="";
function uploadFile() {
  var file = document.querySelector('input[type=file]').files[0];
  var reader  = new FileReader();
  reader.onloadend = function () {
    uploadedImage = reader.result;
    document.getElementById("content").value = encoded_img;
    let contentType = document.getElementById("contentType").value
    if (!uploadedImage.includes(contentType)) {
      alert("Invalid content type")
    }
  if (file) {
    reader.readAsDataURL(file);
  }
  }
}

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

  if (form.contentType == "text/plain" || form.contentType == "text/markdown") {
    form.content = document.getElementById("content").value;
  }

  else if (form.contentType == "image/png;base64" || form.contentType == "image/jpeg;base64") {
    form.content = uploadedImage;
  }

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
  return fetch(url + "/api/posts", {
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
      window.location = url;
    }
    else {
      alert("Error: " + response.status);
    }
  });
}
