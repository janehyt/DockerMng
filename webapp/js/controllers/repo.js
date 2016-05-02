app.controller('RepoListCtrl',['$scope','$http','$state',function($scope,$http,$state){

	$scope.title="仓库列表";
	$scope.repos={};
	$scope.currentPage=2;
	// $scope.pageSize=$state.params.page_size;
	$scope.pageChanged=function(data){
		// console.info(data);
		console.info("changed");
		$scope.loadData(data);
	}

	// console.log($state.params)
	$scope.loadData=function(page){
		var params = $state.params;
		
		params['page']=$scope.currentPage;
		console.info($state.params);
		// params['namespace']='webdevops'
		$http.get("api/repos",{params:params})
			.then(function(response){
				$scope.repos=response.data
			},function(response){
				console.info(response);
			});
	}
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
	$scope.isOfficial=function(namespace){
		return namespace=="library"?true:false
	}
	$scope.detail=function(name,namespace){
		$state.go('app.repo',{name:name,namespace:namespace});
	}
	$scope.loadData();
	

}]);
app.controller('RepoDetailCtrl',['$scope','$http','$state','$sce',function($scope,$http,$state,$sce){

	$scope.title="仓库详情";
	$scope.name = ""
	$scope.data={full_description:"",last_updated:"",pull_count:0};
	$scope.tags={}
	$scope.loadData=function(){	
		$scope.name=($scope.isOfficial($state.params.namespace)?"":$state.params.namespace+"/")+
			$state.params.name	
		$http.get("api/repos/"+$state.params.name+"?namespace="+$state.params.namespace)
			.then(function(response){
				$scope.data=response.data;
				// console.info($scope.data);
			},function(response){
				console.info(response);
			});
	}
	$scope.loadTags=function(){	
		$http.get("api/repos/"+$state.params.name+"/tags"+"?namespace="+$state.params.namespace)
			.then(function(response){
				$scope.tags=response.data;
				console.info($scope.tags);
			},function(response){
				console.info(response);
			});
	}

	$scope.loadHtmlData=function(data){
		return $sce.trustAsHtml($scope.data.full_description);
	}
	$scope.isOfficial=function(namespace){
		return namespace=="library"?true:false
	}
	$scope.time=function(data){
		var ti = data.split("T");
		return ti[0];
	}
	$scope.size=function(data){
		if(!data)
			return "0 B";
		if(data<1024)
			return data+" B"
		if(data<1048576)
			return Math.round(data/1024)+" K"
		return Math.round(data/1048576)+" M"
	}
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
	$scope.publish=function(data){
		var detail = $scope.name+":"+data
		console.info(detail);
	}

	// $scope.loadData();
	// $scope.stateClass = function(status){
	// 	if(status=="running")
	// 		return "label-success"
	// 	else if(status=="ghost")
	// 		return "label-default"
	// 	else
	// 		return "label-warning"
	// }
	

}]);