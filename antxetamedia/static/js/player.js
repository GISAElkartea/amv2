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
      this.currentBlob = null;
      this.playing = false;
    };

    Playlist.prototype.getBlobByUUID = function(blobUUID) {
      for (var i=0; i < this.queue.length; i++) {
        if (this.queue[i].uuid === blobUUID) {
          return this.queue[i];
        }
      }
      return null;
    };

    Playlist.prototype.load = function(blob) {
      this.currentBlob = blob;
      this.audio.src = blob.url;
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

    Playlist.prototype.play = function() {
      this.audio.play();
      this.playing = true;
    };

    Playlist.prototype.next = function() {
    };

    Playlist.prototype.previous = function() {
    };

    Playlist.prototype.extend = function(blobs) {
      Array.prototype.push.apply(this.queue, blobs);
    };

    Playlist.prototype.clear = function() {
      this.queue.splice(0, this.queue.length);
    };

    Playlist.prototype.resume = function(currentBlobUUID, currentTime, playing) {
      this.load(this.getBlobByUUID(currentBlobUUID));
      if (!isNaN(currentTime)) { this.seek(currentTime); }
      if (playing) { this.audio.autoplay = true; }
    };
    return Playlist;
  });


  player.controller('playerController', function($scope, Podcast, Playlist) {
    $scope.playlist = new Playlist();

    var queue = JSON.parse(localStorage.getItem('queue'));
    if (queue) {
      $scope.playlist.queue = queue;
      var currentBlobUUID = localStorage.getItem('currentBlobUUID'),
          currentTime = parseFloat(localStorage.getItem('currentTime')),
          playing = localStorage.getItem('playing');
      if (currentBlobUUID) {
        $scope.playlist.resume(currentBlobUUID, currentTime, playing);
      }
    }

    window.addEventListener('beforeunload', function(event) {
      localStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.currentBlob) {
        localStorage.setItem('currentBlobUUID', $scope.playlist.currentBlob.uuid);
        localStorage.setItem('currentTime', $scope.playlist.audio.currentTime);
        localStorage.setItem('playing', $scope.playlist.playing);
      }
    });

    document.addEventListener('play', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getBlobs().then(function(blobs) {
        $scope.playlist.extend(blobs);
        $scope.playlist.load(blobs[0]);
        $scope.playlist.play();
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
