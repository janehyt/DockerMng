app.controller("SigninCtrl",['$scope',"User","$window",
	function($scope,User,$window){

		$scope.user = {};
		$scope.authError = null;
		$scope.signin = function(){
			User.signin($scope.user).then(
				function(){
					$window.location.reload();
				},
				function(){
					$scope.authError=User.getError();
				});
	}
}]);
