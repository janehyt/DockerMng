app
	.service('User', ['$http','BASE_URL','$q',
		function($http,base_url,$q){
			var __user = {};
			var __error="";
			this.login=function(data){
				var deferred = $q.defer();
				$http.post(base_url+'api/users/sign_in/',data).then(
					function(){
						deferred.resolve();
					},function(x){
						if(x.data.detail&&x.data.detail.indexOf("CSRF")!=-1){
							__error = "您可能已经登陆，请刷新页面";
						}else{							
							__error=x.data;
						}
						deferred.reject(x);
					});
				return deferred.promise;
			}
			this.logout=function(data){
				var deferred = $q.defer();
				$http.post(base_url+"api/users/log_out/")
		            .then(function(){
		              __user = {}
		              deferred.resolve();
		            },function(x){
		            	__error=x.data;
		            	deferred.reject(x);
		            })
		        return deferred.promise;
			}

			this.resetPassword=function(data){
				var deferred = $q.defer();
				$http.post(base_url+"api/users/reset/",data).then(
				function(response){
					deferred.resolve();
				},function(x){
					__error=x.data;
					deferred.reject();
				}
			)
				return deferred.promise;
			}

			this.getError = function(){
				return __error;
			}
			this.getUser = function(){
				
				return __user;
			}
			this.loadUser =function(){
				var deferred = $q.defer();
				
				var deferred = $q.defer();
				$http.get(base_url+"api/users/load_user/")
		            .then(function(response){			              
		              __user=response.data;
		              deferred.resolve();
		            },function(x){
		              deferred.reject();
		            })
				
				return deferred.promise;
			}
			
			
		}]
	);