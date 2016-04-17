app.controller("SigninCtrl",['$scope',"$http","$state","$resource",
	function($scope,$http,$state,$resource){
	$scope.user = {};
	$scope.authError = null;
	$scope.signin = function(){

		$http.post("api/users/sign_in/",$scope.user)
		.then(function(response){
			console.info(response);
		},function(x){
			console.info(x);
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
