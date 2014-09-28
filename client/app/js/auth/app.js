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
            onEnter: function($stateParams, Auth) {
                Auth.confirm($stateParams.token);
            },
        })
});
