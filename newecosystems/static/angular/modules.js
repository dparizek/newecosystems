(function () {
    'use strict';

    var newecosystems = angular.module('newecosystems', ['ui.bootstrap', 'ngAnimate', 'ngGrid', 'ngCookies', 'ui.router', 'restangular', 'tags-input', 'angularFileUpload', 'underscore'])
        .config(['RestangularProvider', '$locationProvider', '$httpProvider', function(RestangularProvider, $locationProvider, $httpProvider) {
            RestangularProvider.setBaseUrl('/api'); // IMPORTANT. needed for Restangular to contact the api.
            RestangularProvider.setRequestSuffix('/'); // IMPORTANT. needed for some api calls that need a trailing /
            //$locationProvider.html5Mode(true); // IMPORTANT. needed for cleaner URLs - disables IE 8/9 support. enable this in production
            //RavenProvider.development(true); // IMPORTANT. sets development mode for Raven, disables logging to Sentry. disable this in production
        }]);

    newecosystems.run([ '$rootScope', '$state', '$stateParams', '$http', '$cookies',
        function($rootScope, $state, $stateParams, $http, $cookies) {
            $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken; // IMPORTANT. needed for django's CSRF protection.
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
        }
    ]);
}());
