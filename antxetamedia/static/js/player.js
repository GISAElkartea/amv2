(function() {
  'use strict';

  var player = angular.module('player', ['ngAudio']);


  player.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });


  player.factory('PodcastBlob', function(NgAudioObject) {
    var PodcastBlob = function(options) {
      this.uuid = options.uuid;
      this.pk = options.pk;
      this.url = options.url;
      this.title = options.title;
      this.image = options.image;
      this.podcast = options.podcast;
      NgAudioObject.call(this, this.url);
    };
    PodcastBlob.prototype = NgAudioObject.prototype;
    PodcastBlob.prototype.constructor = Blob;
    PodcastBlob.prototype.toJSON = function() {
      return {uuid: this.uuid, pk: this.pk, url: this.url, title: this.title,
              image: this.image, podcast: this.podcast};
    };
    return PodcastBlob;
  });


  player.factory('Podcast', function($http, PodcastBlob) {
    var Podcast = function(url) {
      this.url = url;
    };

    Podcast.prototype.getPodcastBlobs = function() {
      return $http.get(this.url).then(function(response) {
        var podcastBlobs = [];
        Array.forEach(response.data, function(data) {
          podcastBlobs.push(new PodcastBlob(data));
        });
        return podcastBlobs;
      });
    };

    return Podcast;
  });


  player.factory('Playlist', function(PodcastBlob) {
    var Playlist = function() {
      this.queue = [];
      this.currentPodcastBlob = null;
      this.playing = false;
    };

    Playlist.prototype.getPodcastBlobByUUID = function(podcastBlobUUID) {
      for (var i=0; i < this.queue.length; i++) {
        if (this.queue[i].uuid === podcastBlobUUID) {
          return this.queue[i];
        }
      }
      return null;
    };

    Playlist.prototype.play = function(podcastBlob) {
      this.currentPodcastBlob = podcastBlob;
      this.currentPodcastBlob.play();
    };

    Playlist.prototype.next = function() {
    };

    Playlist.prototype.previous = function() {
    };

    Playlist.prototype.extend = function(podcastBlobs) {
      Array.prototype.push.apply(this.queue, podcastBlobs);
    };

    Playlist.prototype.clear = function() {
      this.queue.splice(0, this.queue.length);
    };

    return Playlist;
  });


  player.controller('playerController', function($scope, PodcastBlob, Podcast, Playlist) {
    $scope.playlist = new Playlist();

    window.addEventListener('beforeunload', function(event) {
      localStorage.setItem('queue', JSON.stringify($scope.playlist.queue));
      if ($scope.playlist.currentPodcastBlob) {
        localStorage.setItem('currentPodcastBlobUUID', $scope.playlist.currentPodcastBlob.uuid);
        localStorage.setItem('currentTime', $scope.playlist.currentPodcastBlob.currentTime);
        localStorage.setItem('playing', $scope.playlist.playing);
      }
    });

    window.addEventListener('load', function(event) {
      var queue = JSON.parse(localStorage.getItem('queue'));
      if (queue) {
        Array.forEach(queue, function(data) {
          $scope.playlist.queue.push(new PodcastBlob(data));
        });
        var currentPodcastBlobUUID = localStorage.getItem('currentPodcastBlobUUID');
        $scope.playlist.currentPodcastBlob = $scope.playlist.getPodcastBlobByUUID(currentPodcastBlobUUID);
        if ($scope.playlist.currentPodcastBlob && localStorage.getItem('playing')) {
          var currentTime = parseFloat(localStorage.getItem('currentTime'));
          $scope.playlist.currentPodcastBlob.setCurrentTime(currentTime);
          $scope.playlist.play($scope.playlist.currentPodcastBlob);
        }
        window.theplaylist = $scope.playlist;
        $scope.$apply();
      }
    });

    document.addEventListener('play', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getPodcastBlobs().then(function(podcastBlobs) {
        $scope.playlist.extend(podcastBlobs);
        $scope.playlist.play(podcastBlobs[0]);
      });
    });

    document.addEventListener('append', function(event) {
      var podcast = new Podcast(event.detail.podcast);
      podcast.getPodcastBlobs().then(function(podcastBlobs) {
        $scope.playlist.extend(podcastBlobs);
      });
    });
  });
})();
