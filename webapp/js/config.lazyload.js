// lazyload config

angular.module('app')
  // oclazyload config
  .config(['$ocLazyLoadProvider', function($ocLazyLoadProvider) {
      // We configure ocLazyLoad to use the lib script.js as the async loader
      $ocLazyLoadProvider.config({
          debug:  false,
          events: true,
          modules: [
              // {
              //     name: 'ngGrid',
              //     files: [
              //         'app/vendor/modules/ng-grid/ng-grid.min.js',
              //         'app/vendor/modules/ng-grid/ng-grid.min.css',
              //         'app/vendor/modules/ng-grid/theme.css'
              //     ]
              // }
          ]
      });
  }])
;