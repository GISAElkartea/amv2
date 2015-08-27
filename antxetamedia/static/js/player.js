(function() {
  'use strict';

  var player = angular.module('player', ['ngAudio']);

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

  player.factory('Playlist', function(ngAudio) {
    var Playlist = function() {
      this.queue = [];
      this._current = null;
      Object.defineProperty(this, 'current', {
        get: function() { return this._current; },
        set: function(value) { this._current = value; },
      });
    };

    Playlist.prototype.play = function(blob) {
      // Play song
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
    console.log($scope.playlist.current);
    $scope.playlist.current = 2;
    console.log($scope.playlist.current);

    document.addEventListener('play', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      $scope.playlist.clear();
      podcast.getBlobs().then(function(blobs) {
        $scope.playlist.extend(blobs);
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
