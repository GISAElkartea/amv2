angular.module('auth', ['ui.router', 'auth.controllers', 'auth.resources'])

.config(function($stateProvider) {
    $stateProvider
        .state('auth', {
            url: '/auth',
            templateUrl: 'partials/auth.html',
        })
        .state('auth.confirmation', {
            url: '/:token',
            templateUrl: 'partials/auth.confirmation.html',
            onEnter: function($stateParams, AuthService) {
                AuthService.confirm($stateParams.token);
            },
        })
});
