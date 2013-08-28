(function() {
    /**
     * utils
     *
     */
    var foobar = window.foobar || (window.foobar = {
        directives: {},    
        controllers: {},
        mixins: {} /** for $injector.invoke **/
    });
    
    var str30 = function(str) {
        return str.length >=30? str : str+(new Array(30-str.length+1)).join(' ');
    }
    var lineno = 1;
    var digits4 = function(n) {
        var s = ""+n;
        return s.length >= 4 ? s: (new Array(4-s.length+1).join('0'))+s;
    }
    foobar.mixins.DigestWatcher = ['$scope', '$log', function($scope, $log) {
            $scope.$watch(function() {
                //$$phase - $apply | $digest
                var info = [];
                var name = $scope.name || "";
                info.push(digits4(lineno));
                info.push("controller: "+str30(name));
                info.push("scope: "+str30( $scope.$root.$id+"/"+$scope.$id));
                info.push("$$phase: "+str30($scope.$root.$$phase));
                $log.info(info.join(" "));
                lineno +=1;
            });
    }];
})();

/**
 * appMain
 *
 */
(function() {
    angular.module('appMain', []).controller('mainCtrl', ['$scope', '$log', '$injector', function($scope, $log, $injector) {
        $scope.name = "mainCtrl@appMain";
        $scope.brand = "Foobar";
        $scope.title = "foo bar";
        
        $injector.invoke(foobar.mixins.DigestWatcher, this, {$scope: $scope, $log: $log});        
    }]);

    $(function() {
        angular.bootstrap($('#header'), ['appMain']);
    });
})();
