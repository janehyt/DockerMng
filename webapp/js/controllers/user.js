app.controller('UserCtrl',['$scope',function($scope){

	$scope.user={
		name:"admin"
	};

	$scope.logout=function(){
		console.log("logout");
	};
}]);