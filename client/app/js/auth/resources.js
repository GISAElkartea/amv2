angular.module('auth.resources', ['LocalStorageModule', 'app.config'])

.factory('AuthService',
         function(baseUrl, $http, localStorageService) {
             return {
                 getToken: function() {
                     return localStorageService.get('auth_token');
                 },
                 isAuthenticated: function() {
                     return this.getToken() != null;
                 },
                 login: function(credentials) {
                     $http.post(baseUrl + '/auth/token/', credentials)
                     .success(function(result) {
                         localStorageService.set('auth_token', result.token);
                     });
                 },
                 logout: function() {
                     localStorageService.remove('auth_token');
                 },
                 register: function(data) {
                     this.logout();
                     return $http.post(baseUrl + '/auth/user/', data);
                 },
                 confirm: function(token) {
                     $http.put(baseUrl + '/auth/reset/', {'token': token})
                     .success(function(result) {
                         localStorageService.set('auth_token', token);
                     });
                 },
             };
})

.factory('AuthInterceptor', function($q, $injector) {
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
                localStorageService.remove('auth_token');
                $injector.get('$state').go('auth');
            }
            return $q.reject(response);
        }
    };
});
