angular.module('radio.resources', ['app.config'])

.factory('RadioShow', ['baseUrl', '$resource', function(baseUrl, $resource) {
    var url = baseUrl + '/radio/radio/shows/:id/';
    return $resource(url, {'id': '@id'}, {
        'featured': {params: {'featured': 'True'}, isArray: true},
        'nonfeatured': {params: {'featured': 'False'}, isArray: true},
        'categories': {isArray: true},
    }, {stripTrailingSlashes: false});
}]);
