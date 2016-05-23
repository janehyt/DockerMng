app.service('Image',['$http','BASE_URL','$q',
		function($http,base_url,$q){

			var _list=[]
			var _page={page:1,page_size:10,query:''}
			var _url = base_url+"api/images/";
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
			}

			this.pull=function(data){
				
				var deferred = $q.defer();
				$http.post(_url+"pull/",data).then(
					function(response){

						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x.data);
					})
				return deferred.promise;
			}

			this.build=function(data){
				
				var deferred = $q.defer();
				$http.post(_url+"build/",data).then(
					function(response){

						deferred.resolve(response.data);
					},function(x){
						deferred.reject(x.data);
					})
				return deferred.promise;
			}





		}])
	.service('Repo',['$http','BASE_URL','$q',
		function($http,base_url,$q){

			var _list={}
			var _page={page:1,page_size:10,query:'',namespace:''}
			var _url = base_url+"api/repos/";
			var _detail={}
			var _tags={}
			var _tag_page = {page:1,page_size:10}

			this.load=function(namespace,name){
				var deferred = $q.defer();
				$http.get(_url+name,{params:{namespace:namespace}}).then(
					function(response){
						_detail=response.data;
						deferred.resolve(_detail);
					},function(x){
						deferred.reject();
					})
				return deferred.promise;
			}
			this.tags=function(namespace,name){
				var deferred = $q.defer();
				$http.get(_url+name+"/tags",{params:{namespace:namespace,page:_tag_page.page,page_size:_tag_page.page_size}}).then(
					function(response){
						_tags=response.data;
						if(_tags.count>0){
							var num = Math.ceil(_tags.count/_tag_page.page_size);
							_tags.array=new Array(num)
						}
						_tags.page=_tag_page
						deferred.resolve();
					},function(x){
						deferred.reject();
					})
				return deferred.promise;
			}
			this.getTags=function(){
				return _tags
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
			this.getTagPage=function(page){
				return _tag_page;
			}
			this.setTagPage=function(page){
				if(page.page)
					_tag_page.page=page.page;
				if(page.page_size)
					_tag_page.page_size=page.page_size;
			}



		}])
	
;