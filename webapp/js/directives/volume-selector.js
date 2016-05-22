app.directive("volumeSelector", function() {
  return {
    restrict: "EA",
    require: "ngModel",
    replace: true,
    scope: {
      ngModel: "=",
    },
    templateUrl: "app/views/template/volume.html",
    link: function(scope, ele, attr) {
      scope.files = scope.ngModel;
    }
  }
});