// lazyload config

angular.module('app')
  .constant('JQ_CONFIG', {
      // easyPieChart:   ['vendor/jquery/charts/easypiechart/jquery.easy-pie-chart.js'],
      // sparkline:      ['vendor/jquery/charts/sparkline/jquery.sparkline.min.js'],
      plot:           [   'app/vendor/jquery/flot/jquery.flot.min.js', 
                          'app/vendor/jquery/flot/jquery.flot.time.js',
                          'app/vendor/jquery/flot/jquery.flot.resize.js',
                          'app/vendor/jquery/flot/jquery.flot.tooltip.min.js',
                          'app/vendor/jquery/flot/jquery.flot.spline.js',
                          'app/vendor/jquery/flot/jquery.flot.orderBars.js',
                          'app/vendor/jquery/flot/jquery.flot.pie.min.js'],
      })
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