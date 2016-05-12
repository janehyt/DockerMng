app.controller('ApplicationsListCtrl',['$scope','$http','$state','$modal','toaster',
	function($scope,$http,$state,$modal,toaster){

	
	$scope.loadData=function(){
		$http.get("api/containers")
			.then(function(response){
					$scope.containers=response.data;
					console.info($scope.containers);
				},function(x){
					console.info(x);
					// toaster.pop("danger",x.status,x.data);
				});
	}
	
	$scope.stateClass = function(status){
		if(status=="running")
			return "label-success"
		else if(status=="existed"||status=="exited")
			return "label-danger"
		else if(status=="paused"||status=="pulling image")
			return "label-warning"
		else
			return "label-default"
	}
	$scope.search = function(query){
		console.info(query);
	}
	$scope.create = function(){
		$state.go('app.repos');
	}
	$scope.getRepo = function(name){
		name = name.split(":")[0];
		var namespace="library";
		if(name.indexOf("/")!=-1){
			var s =name.split("/")
			namespace=s[0];
			name=s[1];
		}
		var params={
			namespace:namespace,
			name:name
		}
		$state.go('app.repo',params);
	}
	$scope.detail = function(id){
		console.info(id);
		$state.go('app.application',{id:id})
	}
	$scope.delete=function(item){

		var modalIns = $modal.open({
			templateUrl: 'app/views/template/delete.html',
			controller: 'ModalDelCtrl',
			resolve:{
			  name:function(){
			    return item.name;
			  }
			}
		});
		modalIns.result.then(function(){
		// var params = {filename:name,newname:data}
			$http.delete("api/containers/"+item.id+"/").then(
				function(response){
					console.info(response);
					$scope.loadData();
					toaster.pop("success","删除成功","应用"+item.name+"已成功移除！")
			},function(x){
				console.info(x);
				toaster.pop("danger",x.status,x.data)
			})
		},function(){
			console.info("dismiss");
		})

		
	}
	$scope.action=function(a){
		// console.info(a.url)
		$http.get(a.url).then(
			function(response){
				console.info(response);
				$scope.loadData();
				toaster.pop("success",a.name,"操作成功");
			},
			function(x){
				console.info(x);
				toaster.pop("danger",x.status,x.data);
			}
		)
	}

	$scope.title="应用管理";
	$scope.containers=[];
	$scope.loadData();
	

}]);
app.controller('ApplicationCreateCtrl',['$scope','$http','$state','filterOfficialFilter','toaster','$modal',
	function($scope,$http,$state,filterOfficial,toaster,$modal){
		$scope.init=function(){
			$scope.title=filterOfficial($state.params.namespace)+
				$state.params.name;
			$scope.container={image:$scope.title+":"+$state.params.tag}
			$scope.loadLinks();
			$scope.loadFiles();
		};
		$scope.loadLinks=function(){
			$http.get("api/containers/names").then(
				function(response){
					console.info(response.data);
					if(response.data.length>0){
						$scope.link.options=response.data;
						$scope.link.value=$scope.link.options[0];
					}	
				},function(x){
					console.info(x);
				})
		}
		$scope.loadFiles=function(){
			$http.get("api/files").then(
				function(response){
					if(response.data.length>0){
						$scope.volume.options=response.data;
						$scope.volume.select=$scope.volume.options[0].name;
					}
				},function(x){
					console.info(x);
				});
		}

		$scope.confirm=function(){
			var modalIns = $modal.open({
				templateUrl: 'app/views/template/confirm.html',
				controller: 'ModalConCtrl'
			});
			modalIns.result.then(function(){
			// var params = {filename:name,newname:data}
				$scope.publish();
			},function(){
				console.info("dismiss");
			})

		}

		$scope.publish=function(){
			$scope.container.ports=$scope.port.toString();
			$scope.container.envs = $scope.env.toString();
			$scope.container.links=$scope.link.toString();
			$scope.container.volumes = $scope.volume.toString();
			// console.info($scope.container);
			$http.post("api/containers/",$scope.container).then(
				function(response){
					console.info(response);
					var id = response.data.id;
					if(id){
						toaster.pop("success","部署成功","已成功配置应用！");
						$state.go("app.application",{id:id});
					}
				},function(x){
					console.info(x);
				});
		}

		$scope.volume={
			options:null,//文件列表
			select:null,//选中的文件
			value:null,//文件对应的路径
			host:null,//主机路径
			path:null,//容器路径
			
			list:{},//保存的列表
			invalidPath:function(){
				// console.info(this.key,this.value);
				if(this.host&&this.path){
					var key = $.trim(this.host);
					var value = $.trim(this.path);
					if(key.length>0&&value.length>0)
						return value.indexOf("/")!=0;
				}
				return true;
			},
			invalidFile:function(){
				if(this.select&&this.value){
					var key = $.trim(this.select);
					var value = $.trim(this.value);
					if(key.length>0&&value.length>0){
						return value.indexOf("/")!=0;
					}
				}
				return true;
			},
			add:function(value,key){
				//key为容器中路径，value为主机路径或文件名
				this.list[key]={key:key,value:value};
			},
			remove:function(key){
				if(key){
					key=$.trim(key);
					if(this.list[key]){
						delete this.list[key];
					}
				}
			},
			toString:function(){
				var result="";
				for(var e in this.list){
					result+=(this.list[e].value+":"+e);
					
					result+=",";
				}
				if(result!=""){
					result=result.substring(0,result.length-1);
				}
				return result;
			}
		};

		$scope.link={
			options:null,
			key:null,
			value:null,
			list:{},
			invalid:function(){
				// console.info(this.key,this.value);
				if(this.key&&this.value){
					var key = $.trim(this.key);
					var value = $.trim(this.value);
					if(key.length>0&&value.length>0)
						return false;
				}
				return true;
			},
			add:function(){
				var key = $.trim(this.key);
				var value = $.trim(this.value);
				this.list[key]={key:key,value:value};
			},
			remove:function(key){
				if(key){
					key=$.trim(key);
					if(this.list[key]){
						delete this.list[key];
					}
				}
			},
			toString:function(){
				var result="";
				for(var e in this.list){
					result+=(this.list[e].value+":"+e);
					
					result+=",";
				}
				if(result!=""){
					result=result.substring(0,result.length-1);
				}
				return result;
			}
		};

		$scope.env={
			key:null,
			value:null,
			list:{},
			invalid:function(){
				// console.info(this.key,this.value);
				if(this.key&&this.value){
					var key = $.trim(this.key);
					var value = $.trim(this.value);
					if(key.length>0&&value.length>0)
						return false;
				}
				return true;
			},
			add:function(){
				var key = $.trim(this.key);
				var value = $.trim(this.value);
				this.list[key]={key:key,value:value};
			},
			remove:function(key){
				if(key){
					key=$.trim(key);
					if(this.list[key]){
						delete this.list[key];
					}
				}
			},
			toString:function(){
				var result="";
				for(var e in this.list){
					result+=(e+"="+this.list[e].value);
					
					result+=",";
				}
				if(result!=""){
					result=result.substring(0,result.length-1);
				}
				return result;
			}
		};
		$scope.port={
			value:null,
			list:{},
			invalid:function(){
				if(this.value){
					return !(this.value<65535&&this.value>0);
				}
				return true
			},
			add:function(){
				this.list[this.value]={value:this.value,external:false};
				// console.info($scope.ports)
			},
			remove:function(value){
				if(this.list[value])
					delete this.list[value]
				// console.info(value);
			},
			toString:function(){
				var result="";
				for(var p in this.list){
					result+=p;
					if(this.list[p].external){
						result+=":";
					}
					result+=",";
				}
				if(result!=""){
					result=result.substring(0,result.length-1);
				}
				return result;
			}
		};
	
		$scope.init();
	
		// $scope.ports={};


}]);

app.controller('ApplicationDetailCtrl',['$scope','$http','$state','$timeout','$modal','toaster',
	function($scope,$http,$state,$timeout,$modal,toaster){

	$scope.empty=function(data){
		if(data){
			for(var d in data)
				return false;
		}
		return true
	}
	$scope.loadData=function(){	
		$http.get($scope.url).then(
			function(response){
				console.info(response.data);
				$scope.data=response.data;
				$scope.name=$scope.data.name;
				if($scope.data.status.code==2){
					$scope.progress();
				}
			},
			function(x){
				console.info(x);
			}
		);
	}
	$scope.progress=function(){
		$timeout(
			function(){
				$http.get($scope.url+"progress").then(
					function(response){
						
						var progress=response.data;
						$scope.calcuProgress(progress);
						if(progress!='OK'){
							$scope.progress();
						}
					},
					function(x){

					}

				)
			},2000
		);
		
	}
	$scope.stateClass = function(status){
		if(status=="running")
			return "label-success"
		else if(status=="existed"||status=="exited")
			return "label-danger"
		else if(status=="paused"||status=="pulling image")
			return "label-warning"
		else
			return "label-default"
	}
	$scope.delete=function(){

		var modalIns = $modal.open({
			templateUrl: 'app/views/template/delete.html',
			controller: 'ModalDelCtrl',
			resolve:{
			  name:function(){
			    return $scope.name;
			  }
			}
		});
		modalIns.result.then(function(){
		// var params = {filename:name,newname:data}
			$http.delete($scope.url).then(
				function(response){
					console.info(response.data);
					toaster.pop("success","删除成功","应用"+$scope.name+"已成功移除！");
					$state.go("app.applications");
				},
				function(x){
					console.info(x);
					toaster.pop("danger",x.status,x.data);
				}
			);
		},function(){
		console.info("dismiss");
		})

		
	}
	$scope.action=function(a){
		$http.get(a.url).then(
			function(response){
				console.info(response.data);
				$scope.loadData();
				toaster.pop("success",a.name,"操作成功");
			},
			function(x){
				console.info(x);
				toaster.pop("danger",x.status,x.data);
			}
		);
	}
	$scope.calcuProgress=function(data){
		var current=1;
		var total=1;
		var flag=false;
		for(var p in data){
			if(data[p].status=="Downloading"){
				flag=true;
				current+=data[p].detail.current;
				total+=data[p].detail.total;
			}
		}
		if(flag)
			$scope.progressData=(current/total).toFixed(2)*100;
		// console.info($scope.progressData);
	}

	$scope.title="应用列表";
	$scope.name="";
	$scope.url="api/containers/"+$state.params.id+"/";
	$scope.loadData();
	$scope.progressData=0;
	$scope.btnStyle={
		"start": {
			"btn":"btn-success",
			"icon":"fa-play"
		},
		"create":  {
			"btn":"btn-success",
			"icon":"fa-plus"
		},
		"recreate":  {
			"btn":"btn-primary",
			"icon":"fa-refresh"
		},
		"stop":  {
			"btn":"btn-danger",
			"icon":"fa-stop"
		},
		"delete":  {
			"btn":"btn-danger",
			"icon":"fa-trash-o"
		},
		"pause":  {
			"btn":"btn-warning",
			"icon":"fa-pause"
		},
		"unpause":  {
			"btn":"btn-success",
			"icon":"fa-play"
		},
		"restart":  {
			"btn":"btn-primary",
			"icon":"fa-refresh"
		}
	}
	
	

}]);
