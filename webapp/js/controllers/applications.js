app.controller('ApplicationsListCtrl',['$scope','$http','$state','$modal','toaster','$timeout',
	function($scope,$http,$state,$modal,toaster,$timeout){

	
	$scope.loadData=function(url){
		if(!url||url==""){
			if(Math.ceil($scope.page.count/$scope.page.page_size)<
				$scope.page.page){
				$scope.page.page=1
			}
			url="api/containers?page_size="+$scope.page.page_size+
				"&page="+$scope.page.page;
		}
		$scope.containers.previous=null;
		$scope.containers.next=null;
		$http.get(url)
			.then(function(response){
					$scope.containers=response.data;
					$scope.page.count=$scope.containers.count;
					var tmp=url.split("?");
					tmp=tmp[1].split("&");
					for(var t in tmp){
						if(tmp[t].indexOf("page=")==0){
							$scope.page.page=tmp[t].substring(5);
						}
					}
					// console.info($scope.page);
				},function(x){
					console.info(x);
					// toaster.pop("danger",x.status,x.data);
				});
	}
	$scope.getPageArray=function(){
		var num = Math.ceil($scope.page.count/$scope.page.page_size)
		return new Array(num);
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
				toaster.pop("error",x.status,x.data)
			})
		},function(){
			console.info("dismiss");
		})

		
	}
	$scope.action=function(a){
		// console.info(a.url)
		// var m = a.url.indexOf("pull_image/")
		var load = true;
		$http.get(a.url).then(
			function(response){
				console.info(response);
				// if(m!=a.url.length-11){
					load=false
					$scope.loadData();
				// }
				toaster.pop("success",a.name,"操作成功");
			},
			function(x){
				console.info(x);
				toaster.pop("error",x.status,x.data);
				$scope.loadData();
			}
		)
		// if(m==a.url.length-11&&a.name=="create"){
			$timeout(function() {if(load){$scope.loadData()}}, 1000);
		// }
	}

	$scope.title="应用管理";
	$scope.containers=[];
	$scope.page={page:1,page_size:10,count:1}
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
				$scope.resolveInspect();
			},
			function(x){
				console.info(x);
			}
		);
	}
	$scope.progress=function(){
		
				$http.get($scope.url+"progress").then(
					function(response){
						
						var progress=response.data;
						$scope.calcuProgress(progress);
						if(progress!='OK'&&$state.current.name=='app.application'){
							$timeout(
								function(){
									$scope.progress();
							},2000
							);
						}else if(progress=='OK'){
							$scope.loadData();
						}
					},
					function(x){
						console.info(x);
					}

				)
			
		
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
		// var m = a.url.indexOf("pull_image/")
		var load = true;
		$http.get(a.url).then(
			function(response){
				console.info(response.data);
				load=false;
				// if(m!=a.url.length-11){
					$scope.loadData();
				// }
				toaster.pop("success",a.name,"操作成功");
			},
			function(x){
				console.info(x);
				toaster.pop("error",x.status,x.data);
				$scope.loadData();
			}
		);
		// 仅初次pull重新载入
		
			$timeout(function() {if(load){$scope.loadData()}}, 1000);
		
	}
	$scope.calcuProgress=function(data){
		var total=0;
		var count = data.length;
		for(var p in data){
			if(data[p].status){
				if(data[p].status=="Pull complete"||data[p].status=="Download complete"||data[p].status.indexOf("Verifying")!=-1){
					total+=1;
				}
				else if(data[p].detail.current&&data[p].detail.total){
					total+=data[p].detail.current/data[p].detail.total
				}
			}
		}
		if(count>0)
			$scope.progressData=(total/count).toFixed(2)*100;
		// console.info($scope.progressData);
	}
	$scope.resolveInspect=function(){
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
					$scope.inspect.links[name]=data.config.links[name]
				}
			}
			var volumes = data.inspect.Mounts;
			for(var v in volumes){
				var de = volumes[v].Destination;
				var sr = volumes[v].Source;
				if(data.config.volumes[de]){
					sr = data.config.volumes[de].value
				}else{
					sr = "docker volume挂载"
				}
				$scope.inspect.volumes[de]={key:de,value:sr}

			}

		}
	}

	$scope.title="应用列表";
	$scope.name="";
	$scope.url="api/containers/"+$state.params.id+"/";
	$scope.data={};
	$scope.inspect={}
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
	$scope.loadData();
	
	

}]);
