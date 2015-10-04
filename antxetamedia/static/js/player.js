(function() {
  'use strict';

  var player = angular.module('player', ['ngAudio']);


  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  player.factory('Blob', function(NgAudioObject) {
    var Blob = function(options) {
      this.uuid = options.uuid;
      this.pk = options.pk;
      this.url = options.url;
      this.title = options.title;
      this.image = options.image;
      this.podcast = options.podcast;
      NgAudioObject.call(this, this.url);
    };
    Blob.prototype = NgAudioObject.prototype;
    Blob.prototype.constructor = Blob;
    Blob.prototype.toJSON = function() {
      return {uuid: this.uuid, pk: this.pk, url: this.url, title: this.title,
              image: this.image, podcast: this.podcast};
    };
    return Blob;
  });


  player.factory('Podcast', function($http, Blob) {
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


  player.factory('Playlist', function(Blob) {
    var Playlist = function() {
      this.queue = [];
      this.currentBlobUUID = null;
      this.playing = false;
      Object.defineProperty(this, "currentBlob", {
        get: function() {
          var blob = this.getBlobByUUID(this.currentBlobUUID);
          return blob ? new Blob(blob) : null;
        },
        set: function(blob) { this.currentBlobUUID = blob.uuid; },
      });
    };

    Playlist.prototype.getBlobByUUID = function(blobUUID) {
      for (var i=0; i < this.queue.length; i++) {
        if (this.queue[i].uuid === blobUUID) {
          return this.queue[i];
        }
      }
      return null;
    };

    Playlist.prototype.play = function(blob) {
      this.currentBlob = blob;
      this.currentBlob.play();
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

    window.addEventListener('beforeunload', function(event) {
      localStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.currentBlob) {
        localStorage.setItem('currentBlobUUID', $scope.playlist.currentBlobUUID);
        localStorage.setItem('currentTime', $scope.playlist.currentBlob.currentTime);
        localStorage.setItem('playing', $scope.playlist.playing);
      }
    });

    window.addEventListener('load', function(event) {
      var queue = JSON.parse(localStorage.getItem('queue'));
      if (queue) {
        $scope.playlist.queue = queue;
        var currentBlobUUID = localStorage.getItem('currentBlobPk');
        var currentBlob = $scope.playlist.getBlobByUUID(currentBlobUUID);
        if (currentBlob) {
          if (localStorage.getItem('playing')) {
            $scope.playlist.play(currentBlob);
            var currentTime = parseFloat(localStorage.getItem('currentTime'));
            $scope.playlist.currentBlob.setCurrentTime(currentTime);
          }
        }
        window.theplaylist = $scope.playlist;
        $scope.$apply();
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
