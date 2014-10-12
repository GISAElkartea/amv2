angular.module('frontpage', [
    'ui.router',
])

function frontpageConfig($stateProvider) {
    $stateProvider.state('header.frontpage', {
        url: '/',
        title: 'Azala',
        template: '<h1>Frontpage</h1>',
    });
};

angular.module('frontpage').config(frontpageConfig);
