angular.module('radio.controllers', ['radio.resources'])

.controller('RadioShowsController', ['$scope', '$log', 'RadioShow',
            function($scope, $log, RadioShow) {
                $scope.radio_shows = RadioShow.query(function(){
                    console.log($scope.radio_shows);
                });
            }
]);
