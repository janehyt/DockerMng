app.controller('ApplicationsListCtrl',['$scope','$state','$modal',
	'toaster','Container',
	function($scope,$state,$modal,toaster,Container){

	$scope.init = function(){
		$scope.title="容器管理";
		$scope.containers={};
		$scope.loadData();
	}
	
	$scope.loadData=function(page){
		if($scope.containers.page&&page)
			$scope.containers.page.page=page;
		$scope.containers.next=null;
		$scope.containers.previous=null;
		if($scope.containers.page)
			Container.setPage($scope.containers.page);
		Container.list().then(function(){
			$scope.containers=Container.getList();
		})
	}
	// $scope.getPageArray=function(){
	// 	var num = Math.ceil($scope.page.count/$scope.page.page_size)
	// 	return new Array(num);
	// }
	
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
			Container.delete(item.id).then(
				function(data){
					$scope.loadData();
					toaster.pop("success","删除成功","容器"+item.name+"已成功移除！")
				},function(x){
					toaster.pop("error",x.status,x.data)
				})
		},function(){
			console.info("dismiss");
		})

		
	}
	$scope.action=function(a){
		// console.info(a.url)
		// var m = a.url.indexOf("pull_image/")
		Container.action(a.url).then(
			function(data){
				toaster.pop("success",a.name,data);
				$scope.loadData();
			},function(x){
				console.info(x);
				toaster.pop("error",x.status,x.data);
				$scope.loadData();
			})
		// }
	}

	$scope.init();
	
	// $scope.page={page:1,page_size:10,count:1,query:""}
	// $scope.loadData();
	

}]);
app.controller('ApplicationCreateCtrl',['$scope','$state','filterOfficialFilter',
	'toaster','$modal','Image','File','Container',
	function($scope,$state,filterOfficial,toaster,$modal,Image,File,Container){
		$scope.init=function(){
			$scope.container={};
			$scope.title = "镜像仓库";
			$scope.path=""
			Image.load($state.params.id).then(
				function(data){
					// console.info(data);
					$scope.container.image=data.id;
					if(data.repository.indexOf("/")!=-1){
						var repos = data.repository.split("/");
						$scope.params = {namespace:repos[0],name:repos[1]}
					}else{
						$scope.params = {namespace:"library",name:data.repository}
					}
					// console.info($scope.params);
					$scope.tag = data.tag;
				},function(x){
					console.info(x);
				});
			$scope.loadFiles($scope.path);
			$scope.loadOptions()

		}
		$scope.loadFiles = function(path){
	      File.list(path).then(function(){
	        // console.info(File.getFiles());
	        $scope.files = File.getFiles();
	        $scope.path = path;
	        $scope.volume.host=path;
	      });
	    }
		$scope.loadOptions=function(){
			Container.options().then(
				function(data){
					// console.info(data);
					if(data["links"].length>0){
						$scope.link.options=data["links"];
						$scope.link.value=$scope.link.options[0];
					}
					if(data["binds"].length>0){
						$scope.volume.options=data["binds"];
						$scope.volume.select=$scope.volume.options[0];
					}
				},function(x){
					console.info(x);
				})
		}
		
		$scope.selectFile = function(path){
			$scope.volume.host=path;
		}

		$scope.confirm=function(){
			var modalIns = $modal.open({
				templateUrl: 'app/views/template/confirm.html',
				controller: 'ModalConCtrl'
			});
			modalIns.result.then(function(){
				$scope.publish();
			},function(){
				console.info("dismiss");
			})

		}

		$scope.publish=function(){
			$scope.container.ports = $scope.port.toString();
			$scope.container.envs = $scope.env.toString();
			$scope.container.links = $scope.link.toString();
			$scope.container.binds = $scope.volume.toString();
			Container.create($scope.container).then(
				function(data){
					$state.go("app.application",{id:data.id})
				},function(x){
					console.info(x);
					toaster.pop("error",x.status,x.data);
				})
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

app.controller('ApplicationDetailCtrl',['$scope','$state',
	'$timeout','$modal','toaster','uiLoad','JQ_CONFIG','Container',
	function($scope,$state,$timeout,$modal,toaster,uiLoad,JQ_CONFIG,Container){
		// 监控相关
		$scope.stat=function(){
			// console.info($scope.loadStat)
			Container.stat($state.params.id).then(
				function(data){
					$scope.status=data;
					$scope.drawCharts(data);
				},function(x){
					console.info(x);
				});
		}
		$scope.setStat=function(data){
			$scope.loadStat=data;
			if(data==true){
				$scope.stat();
			}
		}

		$scope.drawCharts=function(data){
			var memory=[{label:"free",data:data.memory.limit-data.memory.usage},{label:"usage",data:data.memory.usage}]
			var cpu=[{},{},
				{label:"usermode",data:data.cpu.usermode},
				{label:"kernelmode",data:data.cpu.kernelmode}]
			if($scope.loadStat&&$state.current.name=='app.application'){
				$.plot("#memoryPie",memory,$scope.pieOption);
				$.plot("#cpuPie",cpu,$scope.pieOption);


				// $timeout(function() {$scope.stat()}, 5000);
			}
			
		}

		

		$scope.empty=function(data){
			if(data){
				for(var d in data)
					return false;
			}
			return true
		}
		// 载入数据
		$scope.loadData=function(){	
			Container.load($state.params.id).then(
				function(data){
					
					$scope.data=data;
					$scope.name=$scope.data.name;				
					resolveInspect();

				},
				function(x){
					console.info(x);
				}
			);
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
			Container.delete($state.params.id).then(
				function(data){
					toaster.pop("success","删除成功","容器"+$scope.name+"已成功移除！")
					$state.go("app.applications");
					
				},function(x){
					toaster.pop("error",x.status,x.data)
				});
			},function(){
				console.info("dismiss");
			})			
		}
		$scope.action=function(a){
			Container.action(a.url).then(
				function(data){
					toaster.pop("success",a.name,data);
					$scope.loadData();
				},function(x){
					console.info(x);
					toaster.pop("error",x.status,x.data);
					$scope.loadData();
				})
			// }
		}
		
		var resolveInspect=function(){
			var data = $scope.data;
			if(data.inspect){
				$scope.inspect={
					cmd:data.inspect.Config.Cmd,
					created:data.inspect.Created,
					started:data.inspect.State.StartedAt,
					finished:data.inspect.State.FinishedAt,
					ports:{},
					envs:{},
					ip:data.inspect.NetworkSettings.IPAddress,
					volumes:{},
					links:{}
				}
				var ports = data.inspect.Config.ExposedPorts;
				for(var p in ports){
					var detail="未知"
					if(data.inspect.NetworkSettings.Ports){
						var detail=data.inspect.NetworkSettings.Ports[p];
						if(!$scope.empty(detail)){
							detail=detail[0].HostIp+":"+detail[0].HostPort
						}else{
							detail="内部访问"
						}
					}
					
					$scope.inspect.ports[p]={port:p,detail:detail}
				}
				var envs = data.inspect.Config.Env;
				for(var e in envs){
					var en = envs[e].split("=");
					if(en.length==2)
						$scope.inspect.envs[en[0]]={key:en[0],value:en[1]};
				}
				if(!$scope.inspect.ip){
					$scope.inspect.ip="未知"
				}
				var links = data.inspect.HostConfig.Links;
				for(var l in links){
					var ln=links[l].split(":");
					if(ln.length==2){
						var name = ln[0].substring(1);
						$scope.inspect.links[name]=data.config.links[name];
					}

				}
				console.info($scope.inspect.links,links,data.config.links);
				var volumes = data.inspect.Mounts;
				for(var v in volumes){
					var de = volumes[v].Destination;
					var sr = volumes[v].Source;
					// console.info(data.config.binds)
					if(data.config.binds[de]){
						sr = data.config.binds[de].value;
					}else{
						sr = "docker volume挂载"
					}
					$scope.inspect.volumes[de]={key:de,value:sr}

				}

			}
		}

		

		// $scope.loadStat=false;

		$scope.pieOption={
                series: { pie: { show: true, innerRadius: 0.5, stroke: { width: 0 }, label: { show: true, threshold: 0.05 } } },
                colors: [$scope.app.color.success,$scope.app.color.warning,$scope.app.color.info,$scope.app.color.danger],
                grid: { hoverable: true, clickable: true, borderWidth: 0, color: '#ccc' },   
                tooltip: true,
                tooltipOpts: { content: '%s: %p.0%' }
              }
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
		
		$scope.data={};
		$scope.title="容器列表";
		$scope.name="";
		$scope.status={};
		$scope.inspect={};
		$scope.loadStat=false;

		uiLoad.load(JQ_CONFIG["plot"]).then(function(){

			$scope.loadData();
		});
	

}]);
