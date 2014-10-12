angular.module('radio', [
    'ui.router',

    'radio.controllers'
])

.config(
    function($stateProvider) {
        $stateProvider.state('header.radio', {
            url: '/radio',
            title: 'Irratsaioak',
            views: {
                '': {templateUrl: 'partials/radio.html',
                     controller: 'RadioShowsController'},
            },
        });
})
