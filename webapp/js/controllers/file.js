app.controller('FileCtrl',['$scope','$http','FileUploader',function($scope,$http,FileUploader){

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
      console.info("rename");
    }
    $scope.remove = function(name){
      console.info("remove");
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

    // // FILTERS

    // uploader.filters.push({
    //     name: 'customFilter',
    //     fn: function(item {File|FileLikeObject}, options) {
    //         return this.queue.length < 10;
    //     }
    // });

    // CALLBACKS

    // uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
    //     console.info('onWhenAddingFileFailed', item, filter, options);
    // };
    // uploader.onAfterAddingFile = function(fileItem) {
    //     console.info('onAfterAddingFile', fileItem);
    // };
    // uploader.onAfterAddingAll = function(addedFileItems) {
    //     console.info('onAfterAddingAll', addedFileItems);
    // };
    // uploader.onBeforeUploadItem = function(item) {
    //     console.info('onBeforeUploadItem', item);
    // };
    uploader.onProgressItem = function(fileItem, progress) {
        console.info('onProgressItem', fileItem, progress);
    };
    // uploader.onProgressAll = function(progress) {
    //     console.info('onProgressAll', progress);
    // };
    // uploader.onSuccessItem = function(fileItem, response, status, headers) {
    //     console.info('onSuccessItem', fileItem, response, status, headers);
    // };
    // uploader.onErrorItem = function(fileItem, response, status, headers) {
    //     console.info('onErrorItem', fileItem, response, status, headers);
    // };
    // uploader.onCancelItem = function(fileItem, response, status, headers) {
    //     console.info('onCancelItem', fileItem, response, status, headers);
    // };
    // uploader.onCompleteItem = function(fileItem, response, status, headers) {
    //     console.info('onCompleteItem', fileItem, response, status, headers);
    // };
    // uploader.onCompleteAll = function() {
    //     console.info('onCompleteAll');
    // };

    console.info('uploader', uploader);

    $scope.title="文件管理";

    $scope.files=[];
	

}]);