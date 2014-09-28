'use strict';

// Declare app level module which depends on filters, and services
var App = angular.module('app', [
    'ngSanitize',
    'ngResource',
    'ui.router',

    'app.config',
    'auth',
    'radio',
])

.config(
    function($locationProvider, $urlRouterProvider, $resourceProvider, $httpProvider) {
	// Server side support is needed
	$locationProvider.html5Mode(false);
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $httpProvider.interceptors.push('AuthInterceptor');
	$urlRouterProvider.otherwise('/radio');
    }
);
