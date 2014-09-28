angular.module('radio.controllers', ['radio.resources'])

.controller('RadioShowsController',
            function($scope, $log, RadioShow) {
                $scope.radio_shows = RadioShow.query();
            }
);
