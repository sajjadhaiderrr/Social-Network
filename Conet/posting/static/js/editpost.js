//https://stackoverflow.com/questions/22087076/how-to-make-a-simple-image-upload-using-javascript-html

var form = {
  title: "",
  description: "",
  categories: "",
  contentType: "",
  content: "",
  visibility: "",
  unlisted: "",
  visibleTo: ""
}

function editPage(){
  var postJSON = getPost();
  var data = Promise.resolve(postJSON);
  data.then(function(post) {
  document.getElementById("title").value = form.title = post.title;
  document.getElementById("description").value = form.description = post.description;
  document.getElementById("categories").value = form.categories= post.categories;
  document.getElementById("contentType").value = form.contentType = post.contentType;
  document.getElementById("content").value = form.content = post.content;
  document.getElementById("visibility").value = form.visibility = post.visibility;
  form.unlisted = post.unlisted;
  form.visibleTo = post.visibleTo;
  });
}


function getPost() {
  url = '/posts/'+current_user.postId;
  return fetch(url, {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      redirect: "follow",
      referrer: "no-referrer",
  })
  .then(response => {
    if (response.status === 200) {
      return response.json();
    }
    else {
      alert(response.status);
    }
  });
}

var uploadedImage="";
function uploadFile() {
  var file = document.querySelector('input[type=file]').files[0];
  var reader  = new FileReader();
  reader.onloadend = function () {
    uploadedImage = reader.result;
    let contentType = document.getElementById("contentType").value
    console.log(contentType);
    if (contentType.includes("application/base64")) {
      if (uploadedImage.includes("application") && uploadedImage.includes("base64") ) {
        var continuVar = "";
        document.getElementById("content").value = uploadedImage;
      }
      else {
        alert("Invalid content type")
      }
    }
    else if (!contentType.includes("application/base64")) {
      if (uploadedImage.includes(contentType)) {
        document.getElementById("content").value = uploadedImage;
      }
      else {
        alert("Invalid content type")
      }
    }
  }
  if (file) {
    reader.readAsDataURL(file);
  }
}


function contentEnable() {
  console.log(current_user);
  var checkContentType = document.getElementById("contentType").value;
  if (checkContentType=="text/plain" || checkContentType=="text/markdown") {
    document.getElementById("content").placeholder = "What would you like to share?";
    document.getElementById("content").disabled = false;
    document.getElementById("content").value = "";
  }
  else {
    document.getElementById("content").disabled = true;
    document.getElementById("content").value = "";
    document.getElementById("content").placeholder = "Content is only available for text or markdown posts";
  }
}

function selectFriends() {
    var checkVisibility = document.getElementById("visibility").value;

    if (checkVisibility == "PRIVATE") {
      document.getElementById("selectFriends").disabled = false;
      setFriends();
    }
    else {
      document.getElementById("selectFriends").disabled = true;
      document.getElementById("selectFriends").setAttribute("data-placeholder", "Enabled for Private posts only");
      $('#selectFriends').empty();
      $('#selectFriends').trigger("chosen:updated");
    }
}

function setFriends() {
    getFriends().then(function(response) {
      console.log(response)
      if (response.authors.length == 0) {
        document.getElementById("selectFriends").setAttribute("data-placeholder", "You don't have any friends added");
        $('#selectFriends').trigger("chosen:updated");
      }
      else {
        document.getElementById("selectFriends").setAttribute("data-placeholder", "Start typing to search for friends");
        for (var i = 0; i < response.authors.length; i++) {
          let value =response.authors[i];
          //let innerText=response[i].authors.displayName;
          let option = '<option value='+value+'>'+value+'</option>';
          var newOption = $(option);
          $('#selectFriends').append(newOption);
          $('#selectFriends').trigger("chosen:updated");
        }
    }
    })
}


function editPost() {
  form.title = document.getElementById("title").value;
  form.description = document.getElementById("description").value;
  form.categories = document.getElementById("categories").value;

  form.contentType = document.getElementById("contentType").value;

  if (form.contentType == "text/plain" || form.contentType == "text/markdown") {
    form.content = document.getElementById("content").value;
  }

  else if (form.contentType == "image/png;base64" || form.contentType == "image/jpeg;base64" || form.contentType == "application/base64") {
    if (uploadedImage != "") {
      form.content = uploadedImage;
  }
  }

  form.visibility = document.getElementById("visibility").value;
  form.visibleTo = document.getElementById("selectFriends").value;

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
  postid = url[5];
  url = url[0] + "//" + url[2] ;
  console.log(url + "/posts/edit/"+postid);
  return fetch(url+"/posts/"+postid, {
    method: "PUT",
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
