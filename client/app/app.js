'use strict';

// Declare app level module which depends on filters, and services
var App = angular.module('app', [
    'ngSanitize',
    'ngResource',
    'ui.router',

    'radio',
])

.config([
    '$locationProvider',
    '$urlRouterProvider',
    '$resourceProvider',
    function($locationProvider, $urlRouterProvider, $resourceProvider) {
	// Server side support is needed
	$locationProvider.html5Mode(false);
	$urlRouterProvider.otherwise('/radio');
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }
]);
