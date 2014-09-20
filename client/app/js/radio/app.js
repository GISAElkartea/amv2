angular.module('radio', [
    'ui.router',

    'radio.controllers'
])

.config(['$stateProvider',
        function($stateProvider) {
            $stateProvider.state('radio', {
                url: '/radio',
                data: {pageTitle: 'Radio'},
                templateUrl: 'partials/radio.html',
                controller: 'RadioShowsCtrl',
            });
}])
