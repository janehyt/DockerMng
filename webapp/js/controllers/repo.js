app.controller('RepoListCtrl',['$scope','$http','$state',function($scope,$http,$state){
	// uiLoad.load('app/vendor/libs/moment.min.js');
	
	$scope.loadImages=function(url){
		if(!url){
			if(Math.ceil($scope.page.images.count/$scope.page.images.page_size)<
				$scope.page.images.page){
				$scope.page.images.page=1
			}
			url = "api/images?query="+$scope.page.images.query+"&page_size="+$scope.page.images.page_size+
				"&page="+$scope.page.images.page;
		}
		$scope.images.next=null;
		$scope.images.previous=null;
		$http.get(url)
			.then(function(response){
				$scope.images=response.data;
				$scope.page.images.count=$scope.images.count;
				$scope.page.images.page=$scope.getPageFromUrl(url);
				console.info($scope.images);
			},function(response){
				console.info(response);
			});
	}

	$scope.loadData=function(url){
		if(!url){
			if(Math.ceil($scope.page.repos.count/$scope.page.repos.page_size)<
				$scope.page.repos.page){
				$scope.page.repos.page=1
			}
			url = "api/repos?page_size="+$scope.page.repos.page_size+
				"&page="+$scope.page.repos.page;
		}
		$scope.repos.next=null;
		$scope.repos.previous=null;
		$http.get(url)
			.then(function(response){
				$scope.repos=response.data;
				$scope.page.repos.count=$scope.repos.count;
				$scope.page.repos.page=$scope.getPageFromUrl(url);
				console.info($scope.repos);
			},function(response){
				console.info(response);
			});
	}
	// $scope.otherPage=function(params){
	// 	$state.go('app.repos',params);
	// }
	$scope.getPageFromUrl=function(url){
		var tmp=url.split("?");
		tmp=tmp[1].split("&");
		for(var t in tmp){
			if(tmp[t].indexOf("page=")==0){
				return tmp[t].substring(5);
			}
		}
		return 1
	}
	$scope.getPageArray=function(pagemodel){
		var num = Math.ceil(pagemodel.count/pagemodel.page_size)
		return new Array(num);
	}
	
	// $scope.isOfficial=function(namespace){
	// 	return namespace=="library"?true:false
	// }
	$scope.detail=function(name){
		if(name.indexOf("/")!=-1){
			var list = name.split("/");
			$state.go('app.repo',{name:list[1],namespace:list[0]});
		}else
			$state.go('app.repo',{name:name,namespace:"library"});
	}

	$scope.publish=function(name){
		if(name.indexOf("/")!=-1){
			var list = name.split("/");
			$state.go('app.publish',{name:list[1],namespace:list[0],tag:"latest"});
		}else
			$state.go('app.publish',{name:name,namespace:"library",tag:"latest"});
	}
	$scope.search=function(data){
		if(data&&data.length!=0){
			$scope.page.results={
			page:1,
			page_size:10,
			query:data,
			count:1
			}
			$scope.loadResults();
		}
	}
	$scope.searchImage=function(data){
		$scope.page.images={
			page:1,
			page_size:10,
			query:data,
			count:1
		}
			
			$scope.loadImages();
		
	}
	$scope.loadResults = function(url){
		if(!url){
			if(Math.ceil($scope.page.results.count/$scope.page.results.page_size)<
				$scope.page.results.page){
				$scope.page.results.page=1
			}
			url = "api/repos?query="+$scope.page.results.query+"&page_size="+$scope.page.repos.page_size+
				"&page="+$scope.page.results.page;
			console.info(url);
		}
		$scope.results.next=null;
		$scope.results.previous=null;
		$http.get(url)
			.then(function(response){
				$scope.results=response.data;
				$scope.page.results.count=$scope.results.count;
				$scope.page.results.page=$scope.getPageFromUrl(url);
				console.info($scope.results);
			},function(response){
				console.info(response);
			});
	}
	// $scope.loadData();
	$scope.title="镜像仓库";
	$scope.repos={};
	$scope.results={};
	$scope.images={};
	$scope.page={
		repos:{
			page:1,
			page_size:10,
			count:1
		},
		results:{
			page:1,
			page_size:10,
			query:"",
			count:1
		},
		images:{
			page:1,
			page_size:10,
			query:"",
			count:1
		}
	}
	// $scope.query="";
	

}]);
app.controller('RepoDetailCtrl',['$scope','$http','$state','$sce','filterOfficialFilter',
	function($scope,$http,$state,$sce,filterOfficial){


	$scope.loadData=function(){	
		// console.info("data");
		$scope.tab=1;
		$http.get("api/repos/"+$state.params.name+"?namespace="+$state.params.namespace)
			.then(function(response){
				$scope.data=response.data;
				console.info($scope.data);
			},function(response){
				console.info(response);
			});
	}
	$scope.loadTags=function(url){
		// console.info("tag");
		$scope.tab=2;
		$scope.tags.next=null;
		$scope.tags.previous=null;
		if(!url||url==""){
			if(Math.ceil($scope.page.count/$scope.page.page_size)<
				$scope.page.page){
				$scope.page.page=1
			}
			url = "api/repos/"+$state.params.name+"/tags"+"?namespace="+$state.params.namespace+
				"&page_size="+$scope.page.page_size+"&page="+$scope.page.page;
		}
			
		$http.get(url)
			.then(function(response){
				$scope.tags=response.data;
				$scope.page.count=$scope.tags.count;
				var tmp=url.split("?");
				tmp=tmp[1].split("&");
				for(var t in tmp){
					if(tmp[t].indexOf("page=")==0){
						$scope.page.page=tmp[t].substring(5);
					}
				}
				// console.info($scope.tags);
			},function(response){
				console.info(response);
			});
	}

	$scope.getPageArray=function(){
		var num = Math.ceil($scope.page.count/$scope.page.page_size)
		return new Array(num);
	}
	$scope.loadHtmlData=function(data){
		return $sce.trustAsHtml($scope.data.full_description);
	}
	// $scope.isOfficial=function(namespace){
	// 	return namespace=="library"?true:false
	// }
	
	$scope.publish=function(data){
		// var detail = $scope.name+":"+data
		var params=$state.params;
		params.tag=data;
		console.info(params);
		$state.go('app.publish',params)
		
	}

	$scope.title="镜像仓库";
	$scope.name=filterOfficial($state.params.namespace)+$state.params.name
	$scope.data={full_description:"",last_updated:"",pull_count:0};
	$scope.tags={}
	$scope.page={
		page:1,
		count:1,
		page_size:10
	}
	

}]);