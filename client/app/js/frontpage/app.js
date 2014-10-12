angular.module('frontpage', [
    'ui.router',
])

function frontpageConfig($stateProvider) {
    $stateProvider.state('nav.frontpage', {
        url: '/',
        title: 'Azala',
        template: '<h1>Frontpage</h1>',
    });
};

angular.module('frontpage').config(frontpageConfig);
