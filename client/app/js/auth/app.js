angular.module('auth', ['ui.router', 'auth.controllers', 'auth.resources'])

.config(function($stateProvider) {
    $stateProvider
        .state('nav.auth', {
            url: '/auth',
            title: 'Hasi saioa',
            views: {
                '': {templateUrl: 'partials/auth.html'},
            },
        })
        .state('nav.auth.confirmation', {
            url: '/:token',
            title: 'Kontuaren baieztapena',
            views: {
                '': {templateUrl: 'partials/auth.confirmation.html'},
            },
            onEnter: function($stateParams, AuthService) {
                AuthService.confirm($stateParams.token);
            },
        })
});
