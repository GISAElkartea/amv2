'use strict';

// Declare app level module which depends on filters, and services
var App = angular.module('app', [
    'ngSanitize',
    'ui.router',
    'restangular',

    'app.config',
    'auth',
    'radio',
])

.config(
    function($locationProvider, $urlRouterProvider, $httpProvider, RestangularProvider, baseUrl) {
	// Server side support is needed
	$locationProvider.html5Mode(false);
        RestangularProvider.setBaseUrl(baseUrl);
        $httpProvider.interceptors.push('AuthInterceptor');
	$urlRouterProvider.otherwise('/radio');
    }
);
