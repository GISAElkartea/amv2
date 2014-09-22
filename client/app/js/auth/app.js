angular.module('auth', ['auth.resources'])

.controller('AuthController', ['$scope', 'Auth', function($scope, Auth) {
    $scope.isAuthenticated = function() {
        return Auth.isAuthenticated();
    };

    $scope.getCredentials = function() {
        return {email: $scope.email, password: $scope.password};
    };

    $scope.login = function() {
        Auth.login($scope.getCredentials())
            .catch(function(data) {
                alert(data.data.non_field_errors);
            });
    };

    $scope.logout = function() {
        return Auth.logout();
    };

    $scope.register = function($event) {
        $event.preventDefault();
        Auth.register($scope.getCredentials())
            .catch(function(data) {
                alert(data.data.email);
            });
    };
}]);
