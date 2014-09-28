angular.module('radio.controllers', ['radio.resources'])

.controller('RadioShowsController',
            function($scope, $log, RadioShowService, RadioCategoryService) {
                $scope.featured = RadioShowService.getList({'featured': 'True'}).$object;
                $scope.unfeatured = RadioShowService.getList({'featured': 'False'}).$object;
                $scope.categories = RadioCategoryService.getList().$object;
            }
);
