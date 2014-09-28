angular.module('radio.controllers', ['radio.resources'])

.controller('RadioShowsController',
            function($scope, $log, RadioShowService) {
                $scope.radio_shows = RadioShowService.query();
            }
);
