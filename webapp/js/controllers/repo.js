app.controller('RepoListCtrl',['$scope','$http','$state',function($scope,$http,$state){
	// uiLoad.load('app/vendor/libs/moment.min.js');
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
	$scope.title="镜像仓库";
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
	
	$scope.publish=function(data){
		var detail = $scope.name+":"+data
		console.info(detail);
	}

	$scope.title="镜像仓库";
	$scope.name=($scope.isOfficial($state.params.namespace)?"":$state.params.namespace+"/")+
			$state.params.name
	$scope.data={full_description:"",last_updated:"",pull_count:0};
	$scope.tags={}
	
	

}]);