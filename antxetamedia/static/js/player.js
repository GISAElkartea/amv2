(function() {
  'use strict';

  var player = angular.module('player', []);
  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
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
      this.audio = $document[0].createElement('audio');
      this.queue = [];
      this.current = null;
      this.playing = false;
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

    Playlist.prototype.extend = function(blobs) {
      Array.prototype.push.apply(this.queue, blobs);
    };

    Playlist.prototype.clear = function() {
      this.queue.splice(0, this.queue.length);
    };

    Playlist.prototype.resume = function(position, currentTime, playing) {
      this.load(position);
      if (!isNaN(currentTime)) { this.seek(currentTime); }
      if (playing) { this.audio.autoplay = true; this.playing = true; }
    };
    return Playlist;
  });


  player.controller('playerController', function($scope, Podcast, Playlist) {
    $scope.playlist = new Playlist();

    var queue = JSON.parse(localStorage.getItem('queue'));
    if (queue) {
      $scope.playlist.queue = queue;
      var currentPosition = localStorage.getItem('currentPosition'),
          currentTime = parseFloat(localStorage.getItem('currentTime')),
          playing = localStorage.getItem('playing');
      if (currentPosition !== null) {
        $scope.playlist.resume(currentPosition, currentTime, playing);
      }
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
