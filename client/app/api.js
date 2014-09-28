angular.module('app.$resource', ['ngResource', 'app.config'])

.decorate('$resource', function($delegate, baseUrl) {
    return function() {
        arguments[0] = baseUrl + arguments[0];
        return $delegate.apply(this, arguments);
    };
});
