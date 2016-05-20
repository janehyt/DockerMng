app.controller('ResetCtrl',['$scope','$http','$timeout','$state','User',
	function($scope,$http,$timeout,$state,User){

		$scope.reset=function(){
			$scope.error="";
			User.resetPassword($scope.data).then(
				function(){
					$scope.success="已成功修改密码,稍后请使用新密码重新登陆！";
					$timeout(
						function(){
							$state.go('page.signin');
						},3000
					);
				},function(){
					$scope.error=User.getError();
				})
		}
		$scope.close=function(){
			$scope.success="";
		}
		$scope.title="修改密码";
		$scope.data={};
		$scope.error="";
		$scope.success="";
	

}]);