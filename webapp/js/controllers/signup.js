app.controller("SignupCtrl",['$scope',"User","$window",
	function($scope,User,$window){

		$scope.user = {};
		$scope.authError = null;
		$scope.signup = function(){
			User.signup($scope.user).then(
				function(){
					$window.location.reload();
				},
				function(){
					$scope.authError=User.getError();
				});
	}
}]);