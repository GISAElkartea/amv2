angular.module('auth', ['ui.router', 'auth.controllers', 'auth.resources'])

.config(function($stateProvider) {
    $stateProvider
        .state('header.auth', {
            url: '/auth',
            title: 'Hasi saioa',
            views: {
                '': {templateUrl: 'partials/auth.html'},
            },
        })
        .state('header.auth_confirmation', {
            url: '/auth/:token',
            title: 'Kontuaren baieztapena',
            views: {
                '': {templateUrl: 'partials/auth_confirmation.html'},
            },
            onEnter: function($stateParams, AuthService) {
                AuthService.confirm($stateParams.token);
            },
        })
});
