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
        // Set base url for the API
        RestangularProvider.setBaseUrl(baseUrl);
        // Send JWT headers with every request
        $httpProvider.interceptors.push('AuthInterceptor');
        // Enable CORS
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
        // Default route
	$urlRouterProvider.otherwise('/radio');
    }
);
