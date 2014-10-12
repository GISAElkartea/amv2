angular.module('auth.controllers', ['auth.resources', 'ui.router'])


function mergeErrors(errorTypes) {
    var allErrors = [];
    _(errorTypes).forEach(function(errors) {
        allErrors = _.union(allErrors, errors);
    });
    return allErrors;
};

function LoginController($scope, $state, AuthService) {
    $scope.login = {};

    $scope.getCredentials = function() {
        return {email: $scope.login.email, password: $scope.login.password};
    };

    $scope.isAuthenticated = function() {
        return AuthService.isAuthenticated();
    };

    $scope.login = function() {
        AuthService.login($scope.getCredentials())
            .success(function(data) {
                $state.go('header.frontpage');
            })
            .error(function(data) {
                $scope.login.errors = mergeErrors(data);
            });
    };

    $scope.logout = function() {
        AuthService.logout();
    };
};


function RegistrationController($scope, AuthService) {
    $scope.registration = {};

    $scope.getCredentials = function() {
        return {email: $scope.registration.email, password: $scope.registration.password};
    };

    $scope.validate = function() {
        return $scope.registration.password == $scope.registration.password_check;
    };

    $scope.register = function() {
        if ($scope.validate()) {
            AuthService.register($scope.getCredentials())
                .success(function(data) {
                    $state.go('header.frontpage');
                })
                .error(function(data) {
                    $scope.registration.errors = mergeErrors(data);
                });
        } else {
            $scope.registration.errors = ['Passwords do not match'];
        };
    };
};


angular.module('auth.controllers').controller('LoginController', LoginController);
angular.module('auth.controllers').controller('RegistrationController', RegistrationController);
