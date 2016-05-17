(function() {
  'use strict';

  var player = angular.module('player', ['ngDraggable']);

  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  player.filter('secondsToDate', function() {
    return function(seconds) {
      var date = new Date(0, 0, 0, 0, 0, 0, 0);
      date.setSeconds(seconds);
      return date;
    };
  });


  player.factory('Playlist', function($document) {
    var Playlist = function() {
      var self = this;
      this.audio = $document[0].createElement('audio');
      this.queue = [];
      this.track = null;
      this.playing = false;
      this.audio.addEventListener('ended', function(event) {
        // Only jump to next if it's not the last track
        if (self.track < self.queue.length - 1){
          self.next();
        } else {
          self.playing = false;
        }
      });
    };

    Playlist.prototype.fetch = function(position) {
      if (typeof position !== 'undefined') {
        this.track = position;
      } else if (this.track === null) {
        this.track = 0;
      }
      var newSrc = this.queue[this.track].url;
      // this.audio.src is always an absolute url, newSrc may be not
      if (!this.audio.src || !this.audio.src.endsWith(newSrc)) {
        this.audio.src = newSrc;
      }
    }

    Playlist.prototype.play = function(position) {
      this.fetch(position);
      this.audio.play();
      this.playing = true;
    };

    Playlist.prototype.pause = function() {
      this.audio.pause();
      this.playing = false;
    };

    Playlist.prototype.next = function() {
      this.play((this.track + 1) % this.queue.length);
    };

    Playlist.prototype.previous = function() {
      this.play((this.queue.length + this.track - 1) % this.queue.length);
    };

    Playlist.prototype.remove = function(position) {
      if (position < this.track) {
        this.track -= 1;
      }
      else if (position === this.track) {
        this.pause();
      }
      this.queue.splice(position, 1);
    };

    Playlist.prototype.extend = function(blobs) {
      Array.prototype.push.apply(this.queue, blobs);
    };

    Playlist.prototype.move = function(from, to) {
      var blob = this.queue[from];
      this.queue.splice(from, 1);
      this.queue.splice(to, 0, blob);
      if (this.track == from) {
        this.track = to;
      }
      else if (from < this.track && to >= this.track) {
        this.track--;
      }
      else if (from > this.track && to <= this.track) {
        this.track++;
      }
    };

    Playlist.prototype.save = function() {
      sessionStorage.setItem('queue', JSON.stringify(this.queue));
      if (this.track !== null) {
        sessionStorage.setItem('track', this.track);
        sessionStorage.setItem('time', this.audio.currentTime);
        sessionStorage.setItem('playing', this.playing);
        sessionStorage.setItem('volume', this.audio.volume);
      }
    };

    Playlist.prototype.load = function() {
      var queue = JSON.parse(sessionStorage.getItem('queue')),
          track = sessionStorage.getItem('track'),
          time = parseFloat(sessionStorage.getItem('time')),
          playing = (sessionStorage.getItem('playing') === 'true'),
          volume = sessionStorage.getItem('volume');

      if (!queue || queue.length === 0) {
        this.queue.push(window.STREAM_BLOB);
        this.track = 0;
        return;
      }
      this.queue = queue;

      if (isNaN(track) || 0 > track || track >= queue.length) {
        track = 0;
      }
      this.track = track;
      this.fetch();

      if (isNaN(volume) || volume === null || volume > 1 || volume < 0) {
        volume = 0.5;
      }
      this.audio.volume = volume;

      if (!isNaN(time) && !this.queue[this.track].isStream) {
        this.audio.currentTime = time;
      }

      if (playing) {
        this.play();
      }
    };

    return Playlist;
  });


  player.controller('playerController', function($scope, Playlist) {
    $scope.playlist = new Playlist();
    $scope.playlist.load();

    $scope.setProgress = function(event) {
      var progress = (event.pageX - event.target.getBoundingClientRect().left) / event.target.offsetWidth;
      var time = progress * $scope.playlist.audio.duration;
      if (!isNaN(time)) {
        $scope.playlist.audio.currentTime = time;
      }
    };

    $scope.setVolume = function(volume) {
      $scope.playlist.audio.volume = volume;
    };

    $scope.onDropComplete = function(event, source, destination) {
      $scope.playlist.move(source, destination);
    };

    $scope.playlist.audio.addEventListener('error', function(event) {
      var errno = $scope.playlist.audio.error.code;
      if (errno === MediaError.MEDIA_ERR_NETWORK) {
        window.alert("A network error occurred trying to play this track.");
      }
      else if (errno === MediaError.MEDIA_ERR_DECODE) {
        window.alert("A decodification error occurred trying to play this track.");
      }
      else if (errno === MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED) {
        window.alert("Your browser cannot play this media type.");
      }
    });

    // Update context variables every half a second
    setInterval(function() {
      $scope.blob = $scope.playlist.queue[$scope.playlist.track];
      $scope.time = $scope.playlist.audio.currentTime || 0;
      $scope.volume = $scope.playlist.audio.volume || 0;
      $scope.duration = $scope.playlist.audio.duration || 0;
      $scope.progress = $scope.time * 100 / $scope.duration || 0;
      $scope.$apply();
    }, 500);

    // Save current state before unloading
    window.addEventListener('beforeunload', function(event) {
      $scope.playlist.save();
    });

    document.addEventListener('play', function(event) {
      var position = $scope.playlist.queue.length;
      $scope.playlist.extend(event.detail.blobs);
      $scope.playlist.play(position);
    });

    document.addEventListener('append', function(event) {
      $scope.playlist.extend(event.detail.blobs);
      $scope.playlistDown = true;
    });
  });
})();
