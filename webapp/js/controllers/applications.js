app.controller('ApplicationsListCtrl',['$scope','$http','$state',function($scope,$http,$state){

	
	$scope.loadData=function(){
		$http.get("api/containers")
			.then(function(response){
					$scope.containers=response.data;
					console.info($scope.containers);
				},function(response){
					console.info(data);
				});
	}
	
	$scope.stateClass = function(status){
		if(status=="running")
			return "label-success"
		else if(status=="existed"||status=="exited")
			return "label-danger"
		else if(status=="no instance"||status=="done image")
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
	$scope.detail = function(){

	}
	$scope.delete=function(i){
		$http.delete("api/containers/"+i+"/").then(
			function(response){
				console.info(response);
				$scope.loadData();
		},function(x){
			console.info(x);
		})
	}
	$scope.title="应用管理";
	$scope.containers=[];
	$scope.loadData();
	

}]);
app.controller('ApplicationCreateCtrl',['$scope','$http','$state','filterOfficialFilter',
	function($scope,$http,$state,filterOfficial){
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

		$scope.publish=function(){
			$scope.container.ports=$scope.port.toString();
			$scope.container.envs = $scope.env.toString();
			$scope.container.links=$scope.link.toString();
			$scope.container.volumes = $scope.volume.toString();
			console.info($scope.container);
			$http.post("api/containers/",$scope.container).then(
				function(response){
					console.info(response);
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
