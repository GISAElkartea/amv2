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
    function($locationProvider, $urlRouterProvider) {
	// Server side support is needed
	$locationProvider.html5Mode(false);
	$urlRouterProvider.otherwise('/radio');
    }
]);
