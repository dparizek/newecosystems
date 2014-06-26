/* jshint unused: vars, multistr: true, devel: true, jquery: true, shadow: true */
/* global angular */

(function () {
    'use strict';

    var newecosystems = angular.module('newecosystems');

    newecosystems.controller('HomeCtrl', function ($scope, $stateParams, $state) {
        $state.current.title = 'Home';
    });

    newecosystems.controller('RevertStatusModalCtrl', function ($scope, $modalInstance, status, historyNotes) {
        $scope.ok = function (notes) {
            var eventName = status.status_function_name + 'EventReverted';
            $scope.$emit(eventName, notes);
            $modalInstance.dismiss('ok');
        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });

    newecosystems.controller('ErrorModalCtrl', function ($scope, $modalInstance, err) {
        $scope.err = err;
        $scope.ok = function () {
            $modalInstance.close();
        };
    });
}());
