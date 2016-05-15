(function() {
  'use strict';

  var player = angular.module('player', []);
  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  player.constant('STREAMING_BLOB', {
      'pk': 0,
      'podcast': '/',
      'title': 'Antxeta Irratia zuzenean',
      'image': window.STATIC_URL + 'static/images/radio.svg',
      'url': 'http://streaming.antxetamedia.info:8000/antxetairratia.mp3',
      'isStream': true
  });


  player.filter('secondsToDate', function() {
    return function(seconds) {
      var date = new Date(0, 0, 0, 0, 0, 0, 0);
      date.setSeconds(seconds);
      return date;
    };
  });


  player.factory('Podcast', function($http) {
    var Podcast = function(url) {
      this.url = url;
    };

    Podcast.prototype.getBlobs = function() {
      return $http.get(this.url).then(function(response) {
        return response.data;
      });
    };

    return Podcast;
  });


  player.factory('Playlist', function($document) {
    var Playlist = function() {
      var self = this;
      this.audio = $document[0].createElement('audio');
      this.queue = [];
      this.current = null;
      this.playing = false;
      this.audio.addEventListener('ended', function(event) {
        // Only jump to next if it's not the last track
        if (self.current < self.queue.length - 1){
          self.next();
        } else {
          self.playing = false;
        }
      });
    };

    Playlist.prototype.play = function(position) {
      if (typeof position !== 'undefined') {
        this.current = position;
      } else if (this.current === null) {
        this.current = 0;
      }
      if (typeof position !== 'undefined' || !this.audio.src) {
        this.audio.src = this.queue[this.current].url;
      }
      this.audio.play();
      this.playing = true;
    };

    Playlist.prototype.pause = function() {
      this.audio.pause();
      this.playing = false;
    };

    Playlist.prototype.next = function() {
      this.play((this.current + 1) % this.queue.length);
    };

    Playlist.prototype.previous = function() {
      this.play((this.queue.length + this.current - 1) % this.queue.length);
    };

    Playlist.prototype.remove = function(position) {
      if (position < this.current) {
        this.current -= 1;
      }
      else if (position === this.current) {
        this.pause();
      }
      this.queue.splice(position, 1);
    };

    Playlist.prototype.extend = function(blobs) {
      Array.prototype.push.apply(this.queue, blobs);
    };

    Playlist.prototype.clear = function() {
      this.queue.splice(0, this.queue.length);
    };

    return Playlist;
  });


  player.controller('playerController', function($scope, Podcast, Playlist, STREAMING_BLOB) {
    $scope.playlist = new Playlist();

    // Restore queue or create new one
    var queue = JSON.parse(sessionStorage.getItem('queue'));
    if (queue && queue.length !== 0) {
      $scope.playlist.queue = queue;
    } else {
      $scope.playlist.queue.push(STREAMING_BLOB);
    }

    // Get ready to resume if needed when the audio is loaded
    var currentTime = parseFloat(sessionStorage.getItem('currentTime')),
        playing = (sessionStorage.getItem('playing') === 'true');

    // Cannot be anonymous because we need to remove it as an event listener
    // after it's fired the first time
    function resume(event) {
      if (!isNaN(currentTime)) {
        event.target.fastSeek(currentTime);
      }
      $scope.playlist.audio.removeEventListener('loadeddata', resume);
      $scope.$apply();
    }
    $scope.playlist.audio.addEventListener('loadeddata', resume);

    // Set volume
    var currentVolume = sessionStorage.getItem('volume');
    if (isNaN(currentVolume) || currentVolume === null || currentVolume > 1 || currentVolume < 0) {
      currentVolume = 0.5;
    }
    $scope.playlist.audio.volume = currentVolume;
    $scope.volume = currentVolume;

    // Set current track
    var currentPosition = sessionStorage.getItem('currentPosition');
    if (isNaN(currentPosition) || 0 > currentPosition || !queue || currentPosition >= queue.length) {
      currentPosition = 0;
    }
    $scope.playlist.current = currentPosition;

    // Resume playing
    if (playing) {
      $scope.playlist.play();
    }

    $scope.setProgress = function(event) {
      var progress = (event.pageX - event.target.getBoundingClientRect().x) / event.target.offsetWidth;
      $scope.playlist.audio.fastSeek(progress * $scope.playlist.audio.duration);
    };

    $scope.setVolume = function(volume) {
      $scope.playlist.audio.volume = volume;
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
      $scope.currentBlob = $scope.playlist.queue[$scope.playlist.current];
      $scope.currentTime = $scope.playlist.audio.currentTime || 0;
      $scope.currentDuration = $scope.playlist.audio.duration || 0;
      $scope.currentProgress = $scope.currentTime * 100 / $scope.currentDuration || 0;
      $scope.$apply();
    }, 500);

    // Save current state before unloading
    window.addEventListener('beforeunload', function(event) {
      sessionStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.current !== null) {
        sessionStorage.setItem('currentPosition', $scope.playlist.current);
        sessionStorage.setItem('currentTime', $scope.playlist.audio.currentTime);
        sessionStorage.setItem('playing', $scope.playlist.playing);
        sessionStorage.setItem('volume', $scope.playlist.audio.volume);
      }
    });

    document.addEventListener('play', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getBlobs().then(function(blobs) {
        $scope.playlist.extend(blobs);
        $scope.playlist.play($scope.playlist.queue.length - 1);
      });
    });

    document.addEventListener('append', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getBlobs().then(function(blobs) {
        $scope.playlist.extend(blobs);
        $scope.playlistDown = true;
      });
    });
  });
})();
