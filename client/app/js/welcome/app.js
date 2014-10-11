angular.module('welcome', [
    'ui.router',
])

function welcomeConfig($stateProvider) {
    $stateProvider.state('welcome', {
        url: '/welcome',
        title: 'Ongietorri!',
        views: {
            'body': {templateUrl: 'partials/welcome.html'},
        }
    });
};

angular.module('welcome').config(welcomeConfig);
