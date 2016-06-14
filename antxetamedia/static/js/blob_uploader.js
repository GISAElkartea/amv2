function GetBlobUploader(upload_url, media_url, pending, view) {
  function UploadBlob(field) {
    file = field.files[0];
    field.value = '';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', upload_url.replace('filename', btoa(file.name)), true);
    xhr.setRequestHeader('X-CSRFToken', field.form.csrfmiddlewaretoken.value);
    xhr.upload.status = field.parentNode.firstChild.nextElementSibling; // <span>
    xhr.upload.status.innerHTML = pending;
    xhr.upload.onprogress = function(e) { this.status.innerHTML = Math.round(100 * e.loaded / e.total) + '%'; };
    xhr.onload = function() {
      media_url = media_url.replace('filename', encodeURI(this.responseText));
      this.upload.status.innerHTML = '<a href=\"' + media_url + '\" target=\"_blank\">' + view + '</a>';
      this.upload.status.previousElementSibling.value = this.responseText; // <input type=hidden>
      window.onbeforeunload = function() {};
    };
    window.onbeforeunload = function() { return "Are you sure you want to leave this page?"; };
    xhr.send(file);
  }
  return UploadBlob;
}
