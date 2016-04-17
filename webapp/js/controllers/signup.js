app.controller("SignupCtrl",['$scope',"$http","$state",
	function($scope,$http,$state){
	$scope.user = {};
	$scope.authError = null;
	$scope.signup = function(){
		console.log($scope.user);
	}
	// $scope.login();
}]);