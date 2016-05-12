app.controller('ModalInsCtrl',['$scope','$modalInstance','name',
  function($scope,$modalInstance,name){
    $scope.item = {name:"",suffix:""};
    $scope.init=function(){
      if(name){
        var index = name.lastIndexOf(".")
        if(index!=-1){
          $scope.item.name=name.substring(0,index);
          $scope.item.suffix=name.substring(index);
        }
      }
      
      
    }
    $scope.ok = function () {
      $modalInstance.close($scope.rename+$scope.item.suffix);
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
    $scope.init();

  }]);
app.controller('ModalDelCtrl',['$scope','$modalInstance','name',
  function($scope,$modalInstance,name){
    $scope.name=name;
    
    $scope.ok = function () {
      $modalInstance.close();
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

  }]);

app.controller('ModalConCtrl',['$scope','$modalInstance',
  function($scope,$modalInstance){
    
    $scope.ok = function () {
      $modalInstance.close();
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

  }]);