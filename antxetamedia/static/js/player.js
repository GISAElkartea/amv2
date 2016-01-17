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
      'image': '/favicon.ico',
      'url': 'http://streaming.antxetamedia.info:8000/antxetairratia.mp3'
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

    Playlist.prototype.seek = function(time) {
      var self = this;
      function seek(event) {
        if (!isNaN(time)) { this.fastSeek(time); }
        // Only execute once
        this.removeEventListener('canplay', seek);
      }
      this.audio.addEventListener('canplay', seek);
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

    Playlist.prototype.resume = function(position, currentTime, playing) {
      this.audio.autoplay = this.playing = playing;
      this.load(position);
      if (!isNaN(currentTime)) { this.seek(currentTime); }
    };
    return Playlist;
  });


  player.controller('playerController', function($scope, Podcast, Playlist, STREAMING_BLOB) {
    $scope.playlist = new Playlist();

    var queue = JSON.parse(localStorage.getItem('queue'));
    if (queue && queue.length !== 0) {
      $scope.playlist.queue = queue;
      var currentPosition = localStorage.getItem('currentPosition'),
          currentTime = parseFloat(localStorage.getItem('currentTime')),
          playing = (localStorage.getItem('playing') === 'true');
      if (currentPosition !== null) {
        $scope.playlist.resume(currentPosition, currentTime, playing);
      }
    } else {
      $scope.playlist.queue.push(STREAMING_BLOB);
      $scope.playlist.load(0);
    }

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
        $scope.playlist.play($scope.playlist.queue.length);
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
