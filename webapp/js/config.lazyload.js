// lazyload config

angular.module('app')
  // oclazyload config
  .config(['$ocLazyLoadProvider', function($ocLazyLoadProvider) {
      // We configure ocLazyLoad to use the lib script.js as the async loader
      $ocLazyLoadProvider.config({
          debug:  false,
          events: true,
          modules: [
              {
                  name:'angularFileUpload',
                  files: [
                    'app/vendor/modules/angular-file-upload/angular-file-upload.min.js'
                  ]
              },
              {
                  name: 'toaster',
                  files: [
                      'app/vendor/modules/angularjs-toaster/toaster.js',
                      'app/vendor/modules/angularjs-toaster/toaster.css'
                  ]
              },
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