app.service('Container',['$http','BASE_URL','$q',
		function($http,base_url,$q){

			var _list={}
			var _page={page:1,page_size:10,query:''}
			var _url = base_url+"api/containers/";
			var _detail={}
			
			this.load=function(id){
				var deferred = $q.defer();
				$http.get(_url+id+"/").then(
					function(response){
						_detail=response.data;
						// _resolveConfig(_detail.config)
						deferred.resolve(_detail);
					},function(x){
						deferred.reject();
					})
				return deferred.promise;
			}
			

			this.create=function(data){
				var deferred = $q.defer();
				$http.post(_url,data).then(
					function(response){
						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x);
					});
				return deferred.promise;
			}

			this.list=function(){
				var deferred = $q.defer();
				$http.get(_url,{params:_page}).then(
					function(response){
						_list=response.data;
						if(_list.count>0){
							var num = Math.ceil(_list.count/_page.page_size);
							_list.array=new Array(num)
						}
						_list.page=_page
						deferred.resolve();
					},function(x){
						deferred.reject();
					})
				return deferred.promise;
			}

			this.action = function(url){
				var deferred = $q.defer();
				$http.post(url).then(
					function(response){
						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x);
					});
				return deferred.promise;
			}
			this.delete = function(id){
				var deferred = $q.defer();
				$http.delete(_url+id+"/").then(
					function(response){
						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x);
					});
				return deferred.promise;
			}
			this.options = function(){
				var deferred = $q.defer();
				$http.get(_url+"options/").then(
					function(response){
						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x);
					});
				return deferred.promise;
			}

			this.stat = function(id){
				var deferred = $q.defer();
				$http.get(_url+id+"/stat/").then(
					function(response){
						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x);
					});
				return deferred.promise;
			}

			this.getList=function(){
				return _list
			}
			this.getPage=function(page){
				return _page;
			}
			this.setPage=function(page){
				if(page.page)
					_page.page=page.page;
				if(page.page_size)
					_page.page_size=page.page_size;
				if(page.query)
					_page.query=page.query;
				_page.namespace=page.namespace;
			}


		}])