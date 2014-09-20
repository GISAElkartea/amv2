angular.module('radio', [
    'ui.router',
])

.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('radio', {
        url: '/radio',
        data: {pageTitle: 'Radio'},
        views: {
            "main": {
                templateUrl: '/partials/radio.html'
            }
        }
    });
}]);
