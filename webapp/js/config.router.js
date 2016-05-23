'use strict';

/**
 * Config for the router
 */
angular.module('app')
  .run(['$rootScope', '$state', '$stateParams','$http','User','$window',
      function ($rootScope,   $state,   $stateParams, $http,User,$window) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;
          $rootScope.user = {};
          $rootScope.getUser = function(){
            // console.info("rootscope");
            User.loadUser()
            .then(function(){
              if($state.current.name.indexOf('app.')==0){}                
              else{
                $state.go("app.dashboard");
              }
              $rootScope.user=User.getUser();
              // console.info($rootScope.user);
            },function(){
              if($state.current.name.indexOf('page.')==0){}
              else{
                $state.go("page.signin");
              }
            })
          }

          $rootScope.$on("$stateChangeSuccess", function(event, next, current) {
              $rootScope.getUser();
          });

          // $rootScope.getUser();

          $rootScope.logout = function(){
            User.logout().then(function(){
              $window.location.reload();
            },function(){
              console.info(User.getError());
            })
          }

      }
    ]
  )
  .config(
    [          '$stateProvider', '$urlRouterProvider',
      function ($stateProvider,   $urlRouterProvider) {
          
          $urlRouterProvider
              .otherwise('/app/dashboard');
          $stateProvider
              .state('app', {
                  abstract: true,
                  url: '/app',
                  templateUrl: 'app/views/app.html'
              })
              .state('app.dashboard', {
                  url: '/dashboard',
                  templateUrl: 'app/views/dashboard.html',
              })
              .state('app.reset', {
                  url: '/reset',
                  templateUrl: 'app/views/reset.html',
              })
              // .state('app.applications',{
              //   url: '/applications',
              //   template: '<div ui-view class="fade-in-up"></div>'
              // })
              .state('app.applications', {
                  url: '/applications',
                  templateUrl: 'app/views/applications_list.html',
                  resolve: {
                      deps: ['$ocLazyLoad',
                        function( $ocLazyLoad){
                          return $ocLazyLoad.load('toaster');
                      }]
                  }
              })
              .state('app.application',{
                  url:'/application/:id',
                  templateUrl:'app/views/application_detail.html',
                  resolve: {
                      deps: ['$ocLazyLoad',
                        function( $ocLazyLoad){
                          return $ocLazyLoad.load('toaster');
                      }]
                  }
              })
              .state('app.publish',{
                  url:'/publish/:namespace/:name/:tag',
                  templateUrl:'app/views/application_create.html',
                  resolve: {
                      deps: ['$ocLazyLoad',
                        function( $ocLazyLoad){
                          return $ocLazyLoad.load('toaster');
                      }]
                  }
              })
              .state('app.repos', {
                  url: '/repos?page&page_size&tab',
                  templateUrl: 'app/views/repo_list.html',
              })
              .state('app.repo',{
                url:'/repos/:namespace/:name',
                templateUrl: 'app/views/repo_detail.html',
              })
              .state('app.file', {
                  url: '/file',
                  templateUrl: 'app/views/file.html',
                  resolve: {
                      deps: ['$ocLazyLoad',
                        function( $ocLazyLoad){
                          return $ocLazyLoad.load('angularFileUpload');
                      }]
                  }
              })
              // other pages
              .state('page', {
                  url: '/page',
                  template: '<div ui-view class="fade-in-right-big smooth"></div>'
              })
              .state('page.signin',{
                  url: '/signin',
                  templateUrl: 'app/views/signin.html'
              })
              .state('page.signup',{
                  url: '/signup',
                  templateUrl: 'app/views/signup.html'
              })
              
      }
    ]
  );