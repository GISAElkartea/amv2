angular.module('auth', ['ui.router', 'auth.resources', 'auth.controllers'])

.config(['$stateProvider', function($stateProvider) {
    $stateProvider
        .state('auth', {
            url: '/auth',
            templateUrl: 'partials/auth.html',
        })
}]);
