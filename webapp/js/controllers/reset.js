app.controller('ResetCtrl',['$scope','$http','$timeout','$state',
	function($scope,$http,$timeout,$state){

		$scope.reset=function(){
			$scope.error="";
			$http.post("api/users/reset/",$scope.data).then(
				function(response){
					// alert('已成功修改密码,请使用新密码重新登陆！');
					$scope.success="已成功修改密码,稍后请使用新密码重新登陆！";
					$timeout(
						function(){
							console.info("ok");
							$state.go('page.signin');
						},3000
					);
				},function(x){
					console.info(x);
					$scope.error=x.data;
				}
			)
		}
		$scope.close=function(){
			$scope.success="";
		}
		$scope.title="修改密码";
		$scope.data={};
		$scope.error="";
		$scope.success="";
	

}]);