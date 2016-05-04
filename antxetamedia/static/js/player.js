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
      'image': '/static/images/antxeta.png',
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
      this.audio.addEventListener('ended', function(event) { self.next(); });
    };

    Playlist.prototype.load = function(position) {
      this.current = position;
      this.audio.src = this.queue[position].url;
    };

    Playlist.prototype.play = function(position) {
      if (typeof position !== 'undefined') {
        this.load(position);
      } else if (this.current === null) {
        this.load(0);
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
      if (position === this.current) {
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
    var queue = JSON.parse(localStorage.getItem('queue'));
    if (queue && queue.length !== 0) {
      $scope.playlist.queue = queue;
    } else {
      $scope.playlist.queue.push(STREAMING_BLOB);
    }

    // Get ready to resume if needed when the audio is loaded
    var currentTime = parseFloat(localStorage.getItem('currentTime')),
        playing = (localStorage.getItem('playing') === 'true');
    function resume(event) {
      if (playing) {
        $scope.playlist.play();
      }
      if (!isNaN(currentTime)) {
        event.target.fastSeek(currentTime);
      }
      $scope.playlist.audio.removeEventListener('loadeddata', resume);
      $scope.$apply();
    }
    $scope.playlist.audio.addEventListener('loadeddata', resume);

    // Load the audio
    var currentPosition = localStorage.getItem('currentPosition');
    if (!currentPosition || 0 > currentPosition || currentPosition >= queue.length) {
      currentPosition = 0;
    }
    $scope.playlist.load(currentPosition);

    setInterval(function() {
      $scope.currentBlob = $scope.playlist.queue[$scope.playlist.current];
      $scope.currentTime = $scope.playlist.audio.currentTime;
      $scope.$apply();
    }, 500);

    window.addEventListener('beforeunload', function(event) {
      localStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.current !== null) {
        localStorage.setItem('currentPosition', $scope.playlist.current);
        localStorage.setItem('currentTime', $scope.playlist.audio.currentTime);
        localStorage.setItem('playing', $scope.playlist.playing);
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
      });
    });
  });
})();
