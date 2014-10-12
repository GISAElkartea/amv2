angular.module('auth.resources', ['LocalStorageModule', 'app.config']);


function AuthService(baseUrl, $http, localStorageService) {
    return {
        getToken: function() {
            return localStorageService.get('auth_token');
        },
        isAuthenticated: function() {
            return this.getToken() != null;
        },
        login: function(credentials) {
            var promise = $http.post(baseUrl + '/auth/token/', credentials);
            promise.success(function(result) {
                localStorageService.set('auth_token', result.token);
            });
            return promise;
        },
        logout: function() {
            localStorageService.remove('auth_token');
        },
        register: function(data) {
            this.logout();
            return $http.post(baseUrl + '/auth/user/', data);
        },
        confirm: function(token) {
            var promise = $http.put(baseUrl + '/auth/reset/', {'token': token});
            promise.success(function(result) {
                localStorageService.set('auth_token', token);
            });
            return promise;
        },
    };
};


function AuthInterceptor($q, $injector) {
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
                $injector.get('$state').go('header.auth');
            }
            return $q.reject(response);
        }
    };
};


angular.module('auth.resources').factory('AuthService', AuthService);
angular.module('auth.resources').factory('AuthInterceptor', AuthInterceptor);
