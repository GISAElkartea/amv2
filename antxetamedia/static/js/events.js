(function() {
  function request(method, url) {
    return new Promise(function(resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open(method, url);
      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          resolve(xhr.response);
        } else {
          reject({
            status: this.status,
            statusText: xhr.statusText
          });
        }
      };
      xhr.onerror = function() {
        reject({
          status: this.status,
          statusText: xhr.statusText
        });
      };
      xhr.send();
    });
  }

  function sendPodcast(element, type) {
    var url = element.getAttribute('data-podcast');
    request('GET', url)
    .then(function(data) {
      document.dispatchEvent(new CustomEvent(type, {detail: JSON.parse(data)}));
    });
  }

  var playButtons = document.querySelectorAll('.podcastControl .play');
  Array.from(playButtons).forEach(function(playButton) {
    playButton.onclick = function(event) {
      event.preventDefault();
      sendPodcast(this, 'play');
    };
  });

  var appendButtons = document.querySelectorAll('.podcastControl .append');
  Array.from(appendButtons).forEach(function(appendButton) {
    appendButton.onclick = function(event) {
      event.preventDefault();
      sendPodcast(this, 'append');
    };
  });

  document.getElementById('live').onclick = function(event) {
    event.preventDefault();
    document.dispatchEvent(new CustomEvent('play', {detail: {blobs: [window.STREAM_BLOB]}}));
  };
})();
