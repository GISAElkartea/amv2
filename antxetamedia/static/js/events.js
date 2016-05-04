// Bind play buttons to play events
(function() {
  function sendPlayEvent(event) {
    event.preventDefault();
    var detail = {'podcast': this.getAttribute('data-podcast')};
    var playEvent = new CustomEvent('play', {detail: detail});
    document.dispatchEvent(playEvent);
  }

  var playButtons = document.querySelectorAll('.podcastControl .play');
  Array.from(playButtons).forEach(function(playButton) {
    playButton.onclick = sendPlayEvent;
  });
})();

// Bind append buttons to append events
(function() {
  function sendAppendEvent(event) {
    event.preventDefault();
    var detail = {'podcast': this.getAttribute('data-podcast')};
    var appendEvent = new CustomEvent('append', {detail: detail});
    document.dispatchEvent(appendEvent);
  }

  var appendButtons = document.querySelectorAll('.podcastControl .append');
  Array.from(appendButtons).forEach(function(appendButton) {
    appendButton.onclick = sendAppendEvent;
  });
})();
