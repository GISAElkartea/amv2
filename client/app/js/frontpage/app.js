angular.module('frontpage', [
    'ui.router',
])

function frontpageConfig($stateProvider) {
    $stateProvider.state('yeah', {
        url: '/',
        title: 'Azala',
        template: '<h1>Frontpage</h1>',
    });
};

angular.module('frontpage').config(frontpageConfig);
