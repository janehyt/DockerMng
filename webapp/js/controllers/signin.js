app.controller("SigninCtrl",['$scope',"$http","$state","$resource","$rootScope",
	function($scope,$http,$state,$resource,$rootScope){

		$scope.user = {};
		$scope.authError = null;
		$scope.signin = function(){

			$http.post("api/users/sign_in/",$scope.user)
			.then(function(response){
				// console.info(response);
				if(response.data=="failed"){
					$scope.authError="用户名或密码错误";
				}else{
					$scope.authError="";
					$rootScope.user = response.data;
					window.location.reload();
					// $state.go("app.dashboard");
				}
			},function(x){
				if(x.data.detail&&x.data.detail.indexOf("CSRF")!=-1){
					$scope.authError = "您可能已经登陆，请刷新页面"
				}else{
					console.info(x);
					$scope.authError=x.data;
				}
			})
		// $http({
		// 	url:"api/users/6/",
		// 	method:'DELETE',
		// 	xsrfHeaderName:'X-CSRFToken',
		// 	xsrfCookieName:'csrftoken'
		// }).then(function(response){
		// 	console.info(response);
		// },function(x){
		// 	console.info(x);
		// })
	}
}]);
