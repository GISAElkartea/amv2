angular.module('welcome', [
    'ui.router',
    'auth.controllers'
])

function config($stateProvider) {
    $stateProvider.state('welcome', {
        url: '/',
        data: {pageTitle: 'Welcome'},
        templateUrl: 'partials/welcome.html',
        controller: 'AuthController',
    });
};

angular.module('welcome').config(config);
