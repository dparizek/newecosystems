'use strict';

angular.module('newecosystems')
    .factory('CurrentUser', ['Restangular', function (Restangular) {
        var CurrentUser = Restangular.one('currentuser');
        return CurrentUser;
    }])
    .factory('PlantsForGrid', ['Restangular', function (Restangular) {
        var PlantsForGrid = Restangular.all('allplants');
        return PlantsForGrid;
    }])
    .factory('UploadedFiles', ['Restangular', function (Restangular) {
        var UploadedFiles = Restangular.one('currentuser');
        return UploadedFiles;
    }]);