angular.module('radio.resources', ['app.$resource'])

.factory('RadioShowService', function($resource) {
    return $resource('/radio/radio/shows/:id/', {'id': '@id'}, {
        'featured': {params: {'featured': 'True'}, isArray: true},
        'nonfeatured': {params: {'featured': 'False'}, isArray: true},
        'categories': {isArray: true},
    });
});
