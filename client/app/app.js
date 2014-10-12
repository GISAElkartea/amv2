'use strict';

// Declare app level module which depends on filters, and services
angular.module('app', [
    'ngSanitize',
    'ui.router',
    'restangular',
    'ngFitText',

    'app.config',
    'frontpage',
    'auth',
    'radio',
])

function appConfig($locationProvider, $urlRouterProvider, $httpProvider,
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


function appStates($stateProvider) {
    $stateProvider
        .state('nav', {
            abstract: true,
            views: {
                'nav': {templateUrl: 'partials/nav.html'},
                '': {template: '<ui-view></ui-view>'},
            },
        })
        .state('welcome', {
            url: '/welcome',
            title: 'Ongietorri!',
            views: {
                '': {templateUrl: 'partials/welcome.html'},
            }
        });
};


function appRun($location, $rootScope, $state, AuthService) {
    $rootScope.$on('$stateChangeSuccess', function(event, current, previous) {
        $rootScope.title = current.title;
    });
    // User hits the frontpage and is not authenticated
    if ($location.$$path == '/' && !AuthService.isAuthenticated()) {
        $location.path('/welcome');
        // FIXME: why doesn't it work?
        $state.transitionTo('welcome');
    };
};

angular.module('app').config(appConfig);
angular.module('app').config(appStates);
angular.module('app').run(appRun);
