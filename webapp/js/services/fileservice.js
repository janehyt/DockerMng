app

	.service('File',['$http','BASE_URL','$q','$window',
		function($http,base_url,$q,$window){
			var _files = [];
			var _url = base_url+"api/volumes/";
			this.list=function(path){
				var deferred = $q.defer();
				if(!path){
					path="";
				}
				$http.get(_url,{params:{path:path}}).then(
					function(response){
						_files=response.data;
						console.info(_files);
						deferred.resolve();
					},function(x){
						deferred.reject(x);
					})
				return deferred.promise;
			}
			this.mkdir = function(path,name){
				var deferred = $q.defer();
				if(!path){
					path="";
				}
				$http.post(_url+"mkdir/",{path:path,name:name}).then(
					function(response){
						deferred.resolve();
					},function(x){
						deferred.reject(x);
					})
				return deferred.promise;
			}
			this.unzip = function(path){
				var deferred = $q.defer();
				if(!path){
					path="";
				}
				$http.post(_url+"unzip/",{path:path}).then(
					function(response){
						deferred.resolve();
					},function(x){
						deferred.reject(x);
					})
				return deferred.promise;
			}
			this.download=function(path){
				$window.location=_url+"download/?path="+path;
			}
			this.rename = function(path,name){
				var deferred = $q.defer();
				if(!path){
					path="";
				}
				$http.post(_url+"rename/",{path:path,name:name}).then(
					function(response){
						deferred.resolve();
					},function(x){
						deferred.reject(x);
					})
				return deferred.promise;
			}
			this.remove = function(path){
				var deferred = $q.defer();
				if(!path){
					path="";
				}
				$http.post(_url+"remove/",{path:path}).then(
					function(response){
						deferred.resolve();
					},function(x){
						deferred.reject(x);
					})
				return deferred.promise;
			}
			this.getUploadPath=function(path){
				if(!path){
					path="";
				}
				return _url+"?path="+path;
			}
			this.getFiles = function(){
				return _files;
			}

		}]);