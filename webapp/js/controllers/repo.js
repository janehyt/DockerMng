app.controller('RepoListCtrl',['$scope','$http','$state',function($scope,$http,$state){

	$scope.loadData=function(url){
		if(!url){
			url = "api/repos";
		}
		$scope.repos.next=null;
		$scope.repos.previous=null;
		$http.get(url)
			.then(function(response){
				$scope.repos=response.data;
				console.info($scope.repos);
			},function(response){
				console.info(response);
			});
	}
	$scope.otherPage=function(params){
		$state.go('app.repos',params);
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
		if(data&&data.indexOf("T")){
			var ti = data.split("T");
			return ti[0];
		}
		return data;
	}
	$scope.isOfficial=function(namespace){
		return namespace=="library"?true:false
	}
	$scope.detail=function(name){
		if(name.indexOf("/")!=-1){
			var list = name.split("/");
			$state.go('app.repo',{name:list[1],namespace:list[0]});
		}else
			$state.go('app.repo',{name:name,namespace:"library"});
	}
	$scope.search=function(data){
		console.info(data);
		if(data&&data.length!=0){
			$http.get("api/repos?query="+data)
				.then(function(response){
					$scope.results=response.data
					console.info(response.data);
				},function(response){
					console.info(response);
				});
		}else{
			console.info("null");
		}
	}
	$scope.loadResults = function(url){
		$http.get(url)
			.then(function(response){
				$scope.results=response.data;
				console.info($scope.results);
			},function(response){
				console.info(response);
			});
	}
	// $scope.loadData();
	$scope.title="仓库列表";
	$scope.repos={};
	$scope.results={};
	// $scope.query="";
	

}]);
app.controller('RepoDetailCtrl',['$scope','$http','$state','$sce',function($scope,$http,$state,$sce){


	$scope.loadData=function(){	
		// console.info("data");
		$scope.tab=1;
		$http.get("api/repos/"+$state.params.name+"?namespace="+$state.params.namespace)
			.then(function(response){
				$scope.data=response.data;
				// console.info($scope.data);
			},function(response){
				console.info(response);
			});
	}
	$scope.loadTags=function(url){
		// console.info("tag");
		$scope.tab=2;
		$scope.tags.next=null;
		$scope.tags.previous=null;
		if(!url)
			url = "api/repos/"+$state.params.name+"/tags"+"?namespace="+$state.params.namespace;
		$http.get(url)
			.then(function(response){
				$scope.tags=response.data;
				// console.info($scope.tags);
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
		if(data&&data.indexOf("T")!=-1){
			var ti = data.split("T");
			return ti[0];
		}
		return data
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

	$scope.title="仓库详情";
	$scope.name=($scope.isOfficial($state.params.namespace)?"":$state.params.namespace+"/")+
			$state.params.name
	$scope.data={full_description:"",last_updated:"",pull_count:0};
	$scope.tags={}
	
	

}]);