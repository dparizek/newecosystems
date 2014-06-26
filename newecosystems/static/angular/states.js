(function () {
    'use strict';

    angular.module('newecosystems').config(
        ['$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {

            $urlRouterProvider.otherwise('/');

            $stateProvider
                /* #################################################################### */
                /* ############################## ROOT ################################ */
                /* #################################################################### */
                .state('root', {
                    url: '',
                    abstract: true,
                    templateUrl: '/static/partials/root.html',
                    controller: 'RootCtrl'
                })

                .state('root.plantlist', {
                    url: '/',
                    templateUrl: '/static/partials/plantlist.html',
                    controller: 'PlantCtrl'
                })

                .state('root.about', {
                    url: '/about',
                    templateUrl: '/static/partials/about.html'
                })
                  
                    
            }]);
}());