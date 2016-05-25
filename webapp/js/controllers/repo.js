app.controller('RepoListCtrl',['$scope','$state','Image','Repo','filterOfficialFilter',
	function($scope,$state,Image,Repo,filterOfficialFilter){
	

	$scope.loadImages=function(page){
		if($scope.images.page&&page)
			$scope.images.page.page=page;
		$scope.images.next=null;
		$scope.images.previous=null;
		if($scope.images.page)
			Image.setPage($scope.images.page);
		Image.list().then(function(){
			$scope.images=Image.getList();
		})
	}


	$scope.loadRepos=function(page){
		$scope.repos.page.namespace="local";
		if($scope.repos.page&&page)
			$scope.repos.page.page=page;
		$scope.repos.next=null;
		$scope.repos.previous=null;
		if($scope.repos.page)
			Repo.setPage($scope.repos.page);
		Repo.list().then(function(){
			$scope.repos=Repo.getList();
		})
		
	}

	$scope.loadData=function(page){
		$scope.data.page.namespace="";
		if($scope.data.page&&page)
			$scope.data.page.page=page;
		$scope.data.next=null;
		$scope.data.previous=null;
		if($scope.data.page)
			Repo.setPage($scope.data.page);
		Repo.list().then(function(){
			$scope.data=Repo.getList();
		})
		
	}


	$scope.detail=function(name,namespace){
			$state.go('app.repo',{name:name,namespace:namespace});
	}

	$scope.publish=function(item){
		$state.go('app.publish',{id:item.id})
	}
	$scope.pull=function(name,namespace,tag){
		var repository = filterOfficialFilter(namespace)+name;
		// console.info(repository);
		Image.pull({repository:repository,tag:tag}).then(
			function(data){
				console.info(data);
			},function(x){
				console.info(x);
			})
	}
	$scope.init = function(){
		$scope.title="镜像仓库";
		$scope.repos={page:{namespace:'local'}};
		$scope.images={};
		$scope.data={page:{namespace:''}};
		$scope.tabs=[true,false,false];
		if($state.params.tab){
			$scope.tabs[$state.params.tab]=true;
		}
		$scope.fileService = File;
	}
	$scope.init();
	// $scope.loadData();
	
	// $scope.query="";
	

}]);
app.controller('RepoDetailCtrl',['$scope','$state','$sce',
	'filterOfficialFilter','Repo','Image','File','$modal','toaster',
	function($scope,$state,$sce,filterOfficial,Repo,Image,File,$modal,toaster){


	$scope.loadData=function(){	
		// console.info("data");
		$scope.tab=0;
		Repo.load($state.params.namespace,$state.params.name).then(
			function(data){
				$scope.data=data;
			},function(){})
	}
	$scope.loadTags=function(page){
		// console.info("tag");
		$scope.tab=1;
		if($scope.tags.page&&page)
			$scope.tags.page.page=page;
		$scope.tags.next=null;
		$scope.tags.previous=null;
		if($scope.tags.page)
			Repo.setTagPage($scope.tags.page);
		Repo.tags($state.params.namespace,$state.params.name).then(function(){
			$scope.tags=Repo.getTags();
			console.info($scope.tags);
		})
	}
	$scope.loadFiles = function(path){
		$scope.tab=2;
	  File.list(path).then(function(){
		// console.info(File.getFiles());
		$scope.files = File.getFiles();
		if(path){
		  $scope.path = path;
		}
	  });
	}

	
	$scope.loadHtmlData=function(data){
		return $sce.trustAsHtml($scope.data.full_description);
	}
	$scope.pull=function(data){
		var repository = $scope.name;
		toaster.pop("warning","已开始拉取，可在已有镜像中查看状态。")
		// console.info(repository);
		Image.pull({repository:repository,tag:data}).then(
			function(response){
				console.info(response);
				if($state.current.name=="app.repo"){
					toaster.pop("success","拉取成功");
				}
			},function(x){
				console.info(x);
				if($state.current.name=="app.repo"){
					toaster.pop("error",x);
				}
			});
		
	}
	$scope.publish = function(data){
		
	}
	$scope.create=function(tag){
		var repository = $scope.name;
		toaster.pop("warning","已开始构建，可在已有镜像中查看状态。")
		Image.build({repository:repository,tag:tag,builddir:$scope.path}).then(
			function(response){
				console.info(response,$state.current);
				if($state.current.name=="app.repo"){
					toaster.pop("success","构建成功");
				}
			},function(x){
				console.info(x);
				if($state.current.name=="app.repo"){
					toaster.pop("error",x);
				}
			});
	}
	$scope.rebuild=function(id){
		console.info(response,$state.current);
		Image.rebuild(id).then(
			function(response){
				console.info(response);

			},function(x){
				console.info(x);
			});
	}
	$scope.delete=function(item){
		var modalIns = $modal.open({
			templateUrl: 'app/views/template/delete.html',
			controller: 'ModalDelCtrl',
			resolve:{
				name:function(){
				return item.repository;
			  }
			}
		});
		modalIns.result.then(function(){
			Image.remove(item.id).then(function(){
				toaster.pop("success","已成功移除所选版本");
				$scope.loadTags();
			},function(x){
				console.info(x);
				toaster.pop("error",x);
			})
		},function(){
			console.info("dismiss");
		})

		
	}

	$scope.init=function(){
		$scope.title="镜像仓库";
		$scope.name=filterOfficial($state.params.namespace)+$state.params.name;
		$scope.data={full_description:"",last_updated:"",pull_count:0};
		$scope.tags={};
		$scope.files={};
		$scope.path="";
		// $scope.tabs=[false,false,false];
		// var active = $state.params["tab"] | 0;
		// for(var i in $scope.tabs){
		// 	if(i==active)
		// 		$scope.tabs[i]=true
		// 	else
		// 		$scope.tabs[i]=false
		// }
		$scope.tab=$state.params["tab"];
		// console.info(active);
	}
	$scope.init()
	

}]);

app.controller('RepoCreateCtrl',['$scope','$state','toaster','$modal','Repo',
	function($scope,$state,toaster,$modal,Repo){

		$scope.init=function(){
			$scope.title="镜像仓库";
			$scope.repo={namespace:"local"}
		};

		$scope.confirm=function(){
			var modalIns = $modal.open({
				templateUrl: 'app/views/template/confirm.html',
				controller: 'ModalConCtrl'
			});
			modalIns.result.then(function(){
				Repo.create($scope.repo).then(
					function(data){
						$state.go("app.repo",data);
					},function(x){
						toaster.pop("error",x);
					});
				
			},function(){
				console.info("dismiss");
			})

		}

		$scope.init();

	}
]);