app.controller('FileCtrl',['$scope','FileUploader','$modal','$timeout','File',
  function($scope,FileUploader,$modal,$timeout,File){

    $scope.loadFiles = function(path){
      File.list(path).then(function(){
        // console.info(File.getFiles());
        $scope.files = File.getFiles();
        if(path){
          $scope.path = path;
        }
      });
    }
    $scope.download=function(path){
      File.download(path);
    }
    $scope.unzip=function(path){
      File.unzip(path).then(
          function(){
            $scope.loadFiles($scope.path);
            
          },function(){});
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
        if($scope.path.length>0){
          name = $scope.path+"/"+name;
        }
        File.rename(name,data).then(
          function(){
            $scope.loadFiles($scope.path);
          },function(){});
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
        if($scope.path.length>0){
          name = $scope.path+"/"+name;
        }
        File.remove(name).then(
          function(){
            $scope.loadFiles($scope.path);
          },function(){});
      },function(){
        console.info("dismiss");
      })
    }

    $scope.mkdir=function(name){
      File.mkdir($scope.path,name).then(
        function(){
          $scope.loadFiles($scope.path);
          toaster.pop("success","创建成功");
        },function(){})
    }

	  $scope.setUploader=function(path){
      $scope.uploader.url=File.getUploadPath(path);
      // console.info($scope.uploader.url);
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

    $scope.uploader = new FileUploader({
        url: File.getUploadPath(),
        headers:{'X-CSRFToken':getCookie('csrftoken')},
        // method:'PUT'
    });

    $scope.uploader.onCompleteItem = function(fileItem, response, status, headers) {
       
        if(status==204){
          $timeout(function(){fileItem.remove()},1000);
        }else if(status=403){
          fileItem.error="存在同名文件，不能上传";
        }
         // console.info('onCompleteItem', fileItem, response, status, headers);
        // toaster.pop("success","上传成功");
    };


    $scope.title="文件管理";

    $scope.files=[];
    $scope.path="";
}]);
