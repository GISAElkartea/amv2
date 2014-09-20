angular.module('radio.resources', ['app.config'])

.factory('RadioShow', ['baseUrl', '$resource', function(baseUrl, $resource) {
    return $resource(baseUrl + '/radio/radio/shows/:id');
}]);
