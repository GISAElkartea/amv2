angular.module('auth.controllers', [
    'ui.router',
    'mgo-angular-wizard',
    'auth.resources',
])


function mergeErrors(errorTypes) {
    var allErrors = [];
    _(errorTypes).forEach(function(errors) {
        allErrors = _.union(allErrors, errors);
    });
    return allErrors;
};


function LoginController($scope, $state, WizardHandler, AuthService) {
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
                WizardHandler.wizard().goTo(0);
            });
    };

    $scope.logout = function() {
        AuthService.logout();
    };

    $scope.goBack = function() {
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
                    WizardHandler.wizard().goTo(0);
                });
        } else {
            $scope.registration.errors = ['Passwords do not match'];
            WizardHandler.wizard().goTo(1);
        };
    };
};


angular.module('auth.controllers').controller('LoginController', LoginController);
angular.module('auth.controllers').controller('RegistrationController', RegistrationController);
