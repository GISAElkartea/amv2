'use strict';

// Declare app level module which depends on filters, and services
angular.module('app', [
    'ngSanitize',
    'ui.router',
    'restangular',
    'ngFitText',

    'app.config',
    'welcome',
    'frontpage',
    'auth',
    'radio',
])

appConfig = function($locationProvider, $urlRouterProvider, $httpProvider,
                     RestangularProvider, baseUrl) {
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
                         $urlRouterProvider.otherwise('/');
                     };

angular.module('app').config(appConfig);

appRun = function($location, $rootScope, $state, AuthService) {
    $rootScope.$on('$stateChangeSuccess', function(event, current, previous) {
        $rootScope.title = current.title;
    });
    // User hits the frontpage and is not authenticated
    if ($location.$$path == '/' && !AuthService.isAuthenticated()) {
        $state.go('welcome');
    };
};

angular.module('app').run(appRun);
