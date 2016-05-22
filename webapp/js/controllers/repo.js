app.controller('RepoListCtrl',['$scope','$http','$state','Repo','Hubrepo',
	function($scope,$http,$state,Repo,Hubrepo){
	$scope.fileService = File;
	$scope.loadImages=function(page){
		if($scope.images.page&&page)
			$scope.images.page.page=page;
		$scope.images.next=null;
		$scope.images.previous=null;
		if($scope.images.page)
			Repo.setPage($scope.images.page);
		Repo.list().then(function(){
			$scope.images=Repo.getList();
		})
	}


	$scope.loadData=function(page){
		if($scope.repos.page&&page)
			$scope.repos.page.page=page;
		$scope.repos.next=null;
		$scope.repos.previous=null;
		if($scope.repos.page)
			Hubrepo.setPage($scope.repos.page);
		Hubrepo.list().then(function(){
			$scope.repos=Hubrepo.getList();
		})
		
	}

	$scope.detail=function(name){
		if(name.indexOf("/")!=-1){
			var list = name.split("/");
			$state.go('app.repo',{name:list[1],namespace:list[0]});
		}else
			$state.go('app.repo',{name:name,namespace:"library"});
	}

	$scope.publish=function(item){
		console.info(item);
		// if(name.indexOf("/")!=-1){
		// 	var list = name.split("/");
		// 	$state.go('app.publish',{name:list[1],namespace:list[0],tag:"latest"});
		// }else
		// 	$state.go('app.publish',{name:name,namespace:"library",tag:"latest"});
	}
	$scope.pull=function(item){
		console.info(item);
	}
	// $scope.loadData();
	$scope.title="镜像仓库";
	$scope.repos={page:Hubrepo.getPage()};
	$scope.images={page:Repo.getPage()};
	// $scope.query="";
	

}]);
app.controller('RepoDetailCtrl',['$scope','$http','$state','$sce','filterOfficialFilter','Hubrepo',
	function($scope,$http,$state,$sce,filterOfficial,Hubrepo){


	$scope.loadData=function(){	
		// console.info("data");
		$scope.tab=1;
		Hubrepo.load($state.params.namespace,$state.params.name).then(
			function(data){
				$scope.data=data;
			},function(){})
	}
	$scope.loadTags=function(page){
		// console.info("tag");
		$scope.tab=2;
		if($scope.tags.page&&page)
			$scope.tags.page.page=page;
		$scope.tags.next=null;
		$scope.tags.previous=null;
		if($scope.tags.page)
			Hubrepo.setTagPage($scope.tags.page);
		Hubrepo.tags($state.params.namespace,$state.params.name).then(function(){
			$scope.tags=Hubrepo.getTags();
		})
	}

	
	$scope.loadHtmlData=function(data){
		return $sce.trustAsHtml($scope.data.full_description);
	}
	// $scope.isOfficial=function(namespace){
	// 	return namespace=="library"?true:false
	// }
	
	$scope.pull=function(data){
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
	

}]);