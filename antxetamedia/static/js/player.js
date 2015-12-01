(function() {
  'use strict';

  var player = angular.module('player', ['ngAudio']);


  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  player.factory('Podcast', function($http, ngAudio) {
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


  player.factory('Playlist', function(ngAudio) {
    var Playlist = function() {
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
      blob.audio = ngAudio.load(blob.url);
      return blob;
    };

    Playlist.prototype.play = function(blob) {
      if (blob.audio === undefined) {
        blob = this.load(blob);
      }
      this.currentBlob = blob;
      this.currentBlob.audio.play();
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

    return Playlist;
  });


  player.controller('playerController', function($scope, Podcast, Playlist) {
    $scope.playlist = new Playlist();

    var queue = JSON.parse(localStorage.getItem('queue'));
    if (queue) {
      $scope.playlist.queue = queue;
      var currentBlobUUID = localStorage.getItem('currentBlobUUID');
      if (currentBlobUUID) {
        var blob = $scope.playlist.getBlobByUUID(currentBlobUUID);
        var currentTime = parseFloat(localStorage.getItem('currentTime'));
        blob = $scope.playlist.load(blob);
        $scope.playlist.play(blob);
        window.theplaylist = $scope.playlist;
        console.log(currentTime);
        window.theplaylist.currentBlob.audio.setCurrentTime(currentTime);
        if (localStorage.getItem('playing')) {
        }
      }
    }

    window.addEventListener('beforeunload', function(event) {
      localStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.currentBlob) {
        localStorage.setItem('currentBlobUUID', $scope.playlist.currentBlob.uuid);
        localStorage.setItem('currentTime', $scope.playlist.currentBlob.audio.currentTime);
        localStorage.setItem('playing', $scope.playlist.playing);
      }
    });

    document.addEventListener('play', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getBlobs().then(function(blobs) {
        $scope.playlist.extend(blobs);
        $scope.playlist.play(blobs[0]);
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
