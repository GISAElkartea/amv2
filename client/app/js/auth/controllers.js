angular.module('auth.controllers', ['auth.resources', 'ui.router'])

.controller('AuthController',
    function($scope, $state, $location, AuthService) {
        $scope.isAuthenticated = function() {
            return AuthService.isAuthenticated();
        };

        $scope.getCredentials = function() {
            return {email: $scope.email, password: $scope.password};
        };

        $scope.login = function() {
            AuthService.login($scope.getCredentials())
                .success(function(data) {
                    $state.go('frontpage');
                })
                .error(function(data) {
                    alert(data.data.non_field_errors);
                });
        };

        $scope.logout = function() {
            AuthService.logout();
        };

        $scope.register = function($event) {
            $event.preventDefault();
            AuthService.register($scope.getCredentials())
                .error(function(data) {
                    alert(data.data.email);
                });
        };
});
