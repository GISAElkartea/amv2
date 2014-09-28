angular.module('auth.controllers', ['auth.resources', 'ui.router'])

.controller('AuthController',
    function($scope, Auth, $state) {
        $scope.isAuthenticated = function() {
            return Auth.isAuthenticated();
        };

        $scope.getCredentials = function() {
            return {email: $scope.email, password: $scope.password};
        };

        $scope.login = function() {
            Auth.login($scope.getCredentials())
                .then(function(data) {
                    $state.go('frontpage');
                })
                .catch(function(data) {
                    alert(data.data.non_field_errors);
                });
        };

        $scope.logout = function() {
            Auth.logout();
        };

        $scope.register = function($event) {
            $event.preventDefault();
            Auth.register($scope.getCredentials())
                .catch(function(data) {
                    alert(data.data.email);
                });
        };
});
