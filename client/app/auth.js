angular.module('app.auth', ['app.config'])

.config(['$httpProvider', function($httpProvider) {
    // django and angular both support csrf tokens. This tells
    // angular which cookie to add to what header.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.factory('api', ['baseUrl', '$resource', function(baseUrl, $resource) {
    function add_auth_header(data, headersGetter) {
        // as per HTTP authentication spec [1], credentials must be
        // encoded in base64. Lets use window.btoa [2]
        var headers = headersGetter();
        var auth = data.email + ':' + data.password;
        auth = 'Basic ' + window.btoa(auth);
        headers['Authorization'] = auth;
    }
    return {
        auth: $resource(baseUrl + '/auth/auth/', {}, {
            login: {method: 'POST', transformRequest: add_auth_header},
            logout: {method: 'DELETE'}
        }),
        users: $resource(baseUrl + '/auth/user/', {}, {
            create: {method: 'POST'},
            delete: {method: 'DELETE'}
        })
    };
}])

.controller('AuthController', ['$scope', 'api', function($scope, api) {
    $scope.getCredentials = function() {
        return {email: $scope.email, password: $scope.password};
    };

    $scope.login = function() {
        api.auth.login($scope.getCredentials())
            .$promise
                .then(function(data) {
                    $scope.user = data;
                })
                .catch(function(data) {
                    alert(data.data.detail);
                });
    };

    $scope.logout = function() {
        api.auth.logout(function() {
            $scope.user = undefined;
        });
    };

    $scope.register = function($event) {
        $event.preventDefault();
        api.users.create($scope.getCredentials())
            .$promise
                .then($scope.login)
                .catch(function(data) {
                    alert(data.data.email);
                });
    };
}]);
