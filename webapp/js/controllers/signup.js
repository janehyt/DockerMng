app.controller("SignupCtrl",['$scope',"$http","$state","$rootScope",
	function($scope,$http,$state,$rootScope){

		if($rootScope.user.username){
			$state.go("app.dashboard");
		}

		$scope.user = {};
		$scope.authError = null;
		$scope.signup = function(){

			$http.post("api/users/sign_up/",$scope.user)
			.then(function(response){
				
					$scope.authError="";
					$rootScope.user = response.data;
					$state.go("app.dashboard");
			},function(x){
				var detail = x.data.detail
				if(x.data.detail&&x.data.detail.indexOf("CSRF")!=-1){
					$scope.authError = "您可能已经登陆，请刷新页面"
				}else{
					console.info(x);
					$scope.authError=x.data;
				}
			})
		}
	// $scope.login();
}]);