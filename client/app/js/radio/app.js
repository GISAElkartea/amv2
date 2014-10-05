angular.module('radio', [
    'ui.router',

    'radio.controllers'
])

.config(
    function($stateProvider) {
        $stateProvider.state('radio', {
            url: '/radio',
            title: 'Irratsaioak',
            templateUrl: 'partials/radio.html',
            controller: 'RadioShowsController',
        });
})
