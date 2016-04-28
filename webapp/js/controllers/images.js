app.controller('ImagesListCtrl',['$scope','$http','$state',function($scope,$http,$state){

	$scope.title="Images";
	$scope.images={};

	console.log($state.params)
	$scope.loadData=function(){
		$http.get("api/images/officialRepos",{params:$state.params})
			.then(function(response){
				$scope.images=response.data
				console.info(response.data);
			},function(response){
				console.info(response);
			});
	}
	$scope.loadData();
	$scope.getNumber=function(data){
		var rule = [
			{name:'10M+',min:"10000000"},
			{name:'5M+',min:"5000000"},
			{name:'1M+',min:"1000000"},
			{name:'500K+',min:"500000"},
			{name:'100K+',min:"100000"},
			{name:'50K+',min:"50000"},
			{name:'10K+',min:"10000"}];
		for(var i =0;i<rule.length; i++){
			if(data>rule[i].min){
				return rule[i].name;
			}
		}
		if(data>1000)
			return (data/1000).toFixed(1)+"K";
		return data;


	}
	$scope.time=function(data){
		var ti = data.split("T");
		return ti[0];
	}
	$scope.detail=function(name){
		$state.go('app.image',{name:name});
	}
	// $scope.stateClass = function(status){
	// 	if(status=="running")
	// 		return "label-success"
	// 	else if(status=="ghost")
	// 		return "label-default"
	// 	else
	// 		return "label-warning"
	// }
	

}]);
app.controller('ImageDetailCtrl',['$scope','$http','$state','$sce',function($scope,$http,$state,$sce){

	$scope.title="仓库详情";
	$scope.data={};
	$scope.loadData=function(){
		$http.get("api/images/officialRepos/?name="+$state.params.name)
			.then(function(response){
				$scope.data=response.data;
					console.info(response.data);
				},function(response){
					console.info(response);
				});
	}

	$scope.loadHtmlData=function(data){
		return $sce.trustAsHtml($scope.data.full_description);
	}

	$scope.loadData();
	// $scope.stateClass = function(status){
	// 	if(status=="running")
	// 		return "label-success"
	// 	else if(status=="ghost")
	// 		return "label-default"
	// 	else
	// 		return "label-warning"
	// }
	

}]);