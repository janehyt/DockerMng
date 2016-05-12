app.controller('FileCtrl',['$scope','$http','FileUploader','$modal',
  function($scope,$http,FileUploader,$modal){

    $scope.loadFiles = function(){
      $http.get("api/files").then(function(response){
        $scope.files=response.data;
      },function(response){
        console.info(response);
      })
    }
    $scope.download =function(name){
      console.info(name);;
    }
    $scope.rename = function(name){
      var modalIns = $modal.open({
        templateUrl: 'app/views/template/rename.html',
        controller: 'ModalInsCtrl',
        resolve:{
          name:function(){
            return name;
          }
        }
      });
      modalIns.result.then(function(data){
        // var params = {filename:name,newname:data}
        $http.get("api/files/rename/?filename="+name+"&newname="+data).then(
          function(response){
            console.info(response);
            $scope.loadFiles();
          }
        ),function(x){
          console.info(x);
        }
      },function(){
        console.info("dismiss");
      })
    }
    $scope.remove = function(name){
      var modalIns = $modal.open({
        templateUrl: 'app/views/template/delete.html',
        controller: 'ModalDelCtrl',
        resolve:{
          name:function(){
            return name;
          }
        }
      });
      modalIns.result.then(function(){
        // var params = {filename:name,newname:data}
        $http.get("api/files/remove/?filename="+name).then(
          function(response){
            console.info(response);
            $scope.loadFiles();
          },function(x){
            console.info(x);
          }
        )
      },function(){
        console.info("dismiss");
      })
    }
	  
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    var uploader = $scope.uploader = new FileUploader({
        url: 'api/files/',
        headers:{'X-CSRFToken':csrftoken},
        // method:'PUT'
    });

    uploader.onCompleteItem = function(fileItem, response, status, headers) {
        console.info('onCompleteItem', fileItem, response, status, headers);
        fileItem.remove();
    };

    console.info('uploader', uploader);

    $scope.title="文件管理";

    $scope.files=[];
	

}]);
