angular.module('auth.resources', ['LocalStorageModule', 'app.config'])

.factory('Auth', ['baseUrl', '$http', 'localStorageService',
         function(baseUrl, $http, localStorageService) {
             return {
                 getToken: function() {
                     return localStorageService.get('auth_token');
                 },
                 isAuthenticated: function() {
                     return this.getToken() != null;
                 },
                 login: function(credentials) {
                     var login = $http.post(baseUrl + '/auth/token/', credentials);
                     login.success(function(result) {
                         localStorageService.set('auth_token', result.token);
                     });
                     return login;
                 },
                 logout: function() {
                     localStorageService.remove('auth_token');
                 },
                 register: function(data) {
                     this.logout();
                     var register = $http.post(baseUrl + '/auth/user/', data);
                     var parent = this;
                     register.success(function(result) {
                         parent.login(data);
                     });
                     return register;
                 }
             };
}])

.factory('AuthInterceptor', ['$q', '$injector', function($q, $injector) {
    var localStorageService = $injector.get('localStorageService');
    return {
        request: function(config) {
            var token = localStorageService.get('auth_token');
            if (token) {
                config.headers.Authorization = 'JWT ' + token;
            }
            return config;
        },
        responseError: function(response) {
            if (response.status === 401 || response.status === 403) {
                localStorageService.unset('auth_token');
                $injector.get('$state').go('anon.login');
            }
            return $q.reject(response);
        }
    };
}])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('AuthInterceptor');
}]);
