app.controller('ApplicationsListCtrl',['$scope','$http','$state',function($scope,$http,$state){

	$scope.title="Applications";
	$scope.containers=[];
	$scope.loadData=function(){
		console.log($state.includes("app.applications"))
		$http.get("api/containers")
			.then(function(response){
					$scope.containers=response.data;
					console.info($scope.containers);
				},function(response){
					console.info(data);
				});
	}
	$scope.loadData();
	$scope.stateClass = function(status){
		if(status=="running")
			return "label-success"
		else if(status=="ghost")
			return "label-default"
		else
			return "label-warning"
	}
	

}]);
