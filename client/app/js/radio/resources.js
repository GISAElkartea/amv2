angular.module('radio.resources', ['restangular'])

.factory('RadioShowService', function(Restangular) {
    return Restangular.all('radio').all('radio').all('shows');
})

.factory('RadioCategoryService', function(Restangular) {
    return Restangular.all('radio').all('radio').all('categories');
});
