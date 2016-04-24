var gulp        = require('gulp'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify'),
    jade        = require('gulp-jade'),
    less        = require('gulp-less'),
    path        = require('path'),
    livereload  = require('gulp-livereload'), // Livereload plugin needed: https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei
    changed     = require('gulp-changed'),
    prettify    = require('gulp-html-prettify'),
    rename      = require('gulp-rename'),
    gutil       = require('gulp-util'),
    // htmlify     = require('gulp-angular-htmlify'),
    cleanCSS   = require('gulp-clean-css'),
    // gulpFilter  = require('gulp-filter'),
    // expect      = require('gulp-expect-file'),
    gulpsync    = require('gulp-sync')(gulp),
    ngAnnotate  = require('gulp-ng-annotate'),
    sourcemaps  = require('gulp-sourcemaps'),
    PluginError = gutil.PluginError;

// LiveReload port. Change it only if there's a conflict
var lvr_port = 35729;


var useSourceMaps = true;

// ignore everything that begins with underscore
var hidden_files = '**/_*.*';
var ignored_files = '!'+hidden_files;

//VENDOR

// var vendor = {
//   angular:{
//     source: [
//       "bower_components/angular/angular.js",
//       "bower_components/angular-animate/angular-animate.js",
//       "bower_components/angular-cookies/angular-cookies.js",
//       "bower_components/angular-resource/angular-resource.js",
//       "bower_components/angular-sanitize/angular-sanitize.js",
//       "bower_components/angular-touch/angular-touch.js",
//       // "bower_components/bootstrap/dist/js/bootstrap.js", 
//       "bower_components/angular-ui-router/release/angular-ui-router.js",
//       "bower_components/angular-bootstrap/ui-bootstrap-tpls.js",
//       "bower_components/angular-translate/angular-translate.js", 
//       "bower_components/angular-ui-utils/ui-utils.js",
//       "bower_components/ngstorage/ngStorage.js",
//       "bower_components/oclazyload/dist/ocLazyLoad.js"
//     ],
//     dest: "vendor/angular"
//   },
//   rename: {
//     source:[
//       "bower_components/angular-translate-storage-cookie/angular-translate-storage-cookie.js",
//       "bower_components/angular-translate-storage-local/angular-translate-storage-local.js",
//       "bower_components/angular-translate-loader-static-files/angular-translate-loader-static-files.js"    
//     ],
//     dest:"vendor/angular"
//   },
//   jquery: {
//     source: "bower_components/jquery/dist/jquery.js",
//     dest: "vendor/jquery"
//   },
//   libs: {
//     source: [
//       "bower_components/moment/min/moment.min.js",
//       "bower_components/screenfull/dist/screenfull.min.js"
//     ],
//     dest: "../mysite/dist/app/vendor/libs"
// //   },
// //   modules: {

//   }
// }

// SOURCES CONFIG 
var source = {
  scripts: {
    base: [
              'vendor/jquery/jquery.js',
              'vendor/angular/angular.js',
              'vendor/angular/**/*.js',

    ],
    app:    [ 
              'js/*.js',
              'js/**/*.js',
            ],
    watch: ['js/**/*.js',
            'js/*.js'
           ]
  },
  styles: {
    less: 'css/less/app.less', 
    dir: 'css/less',
    css: ['css/bootstrap.css','css/*.css'],
    watch: {
      less:'css/less/*.less', 
      css: 'css/*.css'
    }
  },
  templates: {
    app: {
        files : ['jade/index.jade'],
        watch: ['jade/index.jade', 'head.jade','scripts.jade']
    },
    views: {
        files : ['jade/views/*.jade', 'jade/views/**/*.jade', ignored_files],
        watch: ['jade/views/**/*.jade','jade/views/*.jade']
    }
  },
  img: {
    files: ['img/*.jpg',
            'img/*.png',
            'img/*.ico']
  },
  lang: {
    files: 'l10n/*.js'
  },
  fonts: {
    files:  ['fonts/*',
             'fonts/**/*']
  },
  vendor: {
    files: 'vendor/**/*.js',
  }
  
};

//TARGET CONFUG
var dist = {
  watch: ['../mysite/dist/**','../mysite/dist/app/**'],
  scripts: {
    base: 'base.js',
    app: 'app.js',
    dir: '../mysite/dist/app/js'
  },
  templates: {
    app: '../mysite/dist',
    views: '../mysite/dist/app/views',
  },
  styles: {
    dir: '../mysite/dist/app/css',
    main: 'app.css',
    less: 'css'
  },
  img: {
    dir: '../mysite/dist/app/img'
  },
  lang: {
    dir: '../mysite/dist/app/l10n'
  },
  fonts: {
    dir:  '../mysite/dist/app/fonts'
  },
  vendor: {
    dir: '../mysite/dist/app/vendor'
  }
}

// //vendor
// gulp.task('vendor:angular',function(){
//   return gulp.src(vendor.angular.source)
//       .pipe(gulp.dest(vendor.angular.dest))
// });
// gulp.task('vendor:rename',function(){
//   return gulp.src(vendor.rename.source)
//       .pipe(rename({prefix:"tran-"}))
//       .pipe(gulp.dest(vendor.rename.dest))
// });
// gulp.task('vendor:jquery',function(){
//   return gulp.src(vendor.jquery.source)
//       .pipe(gulp.dest(vendor.jquery.dest))
// });
// gulp.task('vendor:libs',function(){
//   return gulp.src(vendor.libs.source)
//       .pipe(gulp.dest(vendor.libs.dest))
// });
// gulp.task('vendor',['vendor:angular','vendor:rename','vendor:jquery','vendor:libs']);
//copy
gulp.task('copy:img',function(){
  return gulp.src(source.img.files)
      .pipe(gulp.dest(dist.img.dir))
});
gulp.task('copy:fonts',function(){
  return gulp.src(source.fonts.files)
      .pipe(gulp.dest(dist.fonts.dir))
});
gulp.task('copy:lang',function(){
  return gulp.src(source.lang.files)
      .pipe(gulp.dest(dist.lang.dir))
});
gulp.task('copy:vendor',function(){
  return gulp.src(source.vendor.files)
      .pipe(gulp.dest(dist.vendor.dir))
});
gulp.task('copy',['copy:img','copy:fonts','copy:lang','copy:vendor'])

//---------------
// TASKS
//---------------

// JS APP
gulp.task('scripts:base', function() {
    // Minify and copy all JavaScript (except vendor scripts)
    return gulp.src(source.scripts.base)
        .pipe( useSourceMaps ? sourcemaps.init() : gutil.noop())
        .pipe(concat(dist.scripts.base))
        .pipe(ngAnnotate())

        .on("error", handleError)
        .pipe(gulp.dest(dist.scripts.dir))
        // .on("error", handleError)
        .pipe( useSourceMaps ? sourcemaps.write() : gutil.noop() )
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(dist.scripts.dir))
        // .pipe(gulp.dest(build.scripts.app.server_dir));
});

// JS APP
gulp.task('scripts:app', function() {
    // Minify and copy all JavaScript (except vendor scripts)
    return gulp.src(source.scripts.app)
        .pipe( useSourceMaps ? sourcemaps.init() : gutil.noop())
        .pipe(concat(dist.scripts.app))
        .pipe(ngAnnotate())

        .on("error", handleError)
        .pipe(gulp.dest(dist.scripts.dir))
        // .on("error", handleError)
        .pipe( useSourceMaps ? sourcemaps.write() : gutil.noop() )
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest(dist.scripts.dir))
        // .pipe(gulp.dest(build.scripts.app.server_dir));
});


// APP LESS
gulp.task('styles:app', function() {
    return gulp.src(source.styles.less)
        .pipe( useSourceMaps ? sourcemaps.init() : gutil.noop())
        .pipe(less({
            paths: [source.styles.dir]
        }))
        .on("error", handleError)
        .pipe( useSourceMaps ? sourcemaps.write() : gutil.noop())
        .pipe(gulp.dest(dist.styles.less));
});
gulp.task('styles:min',function(){
    return gulp.src(source.styles.css)
        .pipe( useSourceMaps ? sourcemaps.init() : gutil.noop())
        .pipe(concat(dist.styles.main))
        .pipe(rename({suffix: '.min'}))
        .pipe(cleanCSS())
        .on("error", handleError)
        .pipe( useSourceMaps ? sourcemaps.write() : gutil.noop())
        .pipe(gulp.dest(dist.styles.dir))
})


// JADE
gulp.task('templates:app', function() {
    return gulp.src(source.templates.app.files)
        .pipe(changed(dist.templates.app, { extension: '.html' }))
        .pipe(jade())
        .on("error", handleError)
        .pipe(prettify({
            indent_char: ' ',
            indent_size: 3,
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']
        }))
        .pipe(gulp.dest(dist.templates.app))
        ;
});
gulp.task('templates:views', function() {
    return gulp.src(source.templates.views.files)
        .pipe(changed(dist.templates.views, { extension: '.html' }))
        .pipe(jade())
        .on("error", handleError)
        .pipe(prettify({
            indent_char: ' ',
            indent_size: 3,
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']
        }))
        .pipe(gulp.dest(dist.templates.views))
        ;
});


//---------------
// WATCH
//---------------

// Rerun the task when a file changes
gulp.task('watch', function() {
  livereload.listen();

  gulp.watch(source.scripts.watch,            ['scripts:app']);
  gulp.watch(source.templates.views.watch,    ['templates:views']);
  gulp.watch(source.templates.app.watch,      ['templates:app']);
  gulp.watch(source.styles.watch.less,        ['styles:app']);
  gulp.watch(source.styles.watch.css,         ['styles:min']);
  // gulp.watch(source.img.files,                ['copy:img']);
  // gulp.watch(source.fonts.files,              ['copy:fonts']);
  gulp.watch(source.lang.files,               ['copy:lang']);
  gulp.watch(dist.watch).on('change', function(event) {

      livereload.changed( event.path );

  });

});


//---------------
// DEFAULT TASK
//---------------


// build for production (minify)
gulp.task('build', ['default']);


// build with sourcemaps (no minify)
gulp.task('sourcemaps', ['usesources', 'default']);
gulp.task('usesources', function(){ useSourceMaps = true; });

// default (no minify)
gulp.task('default', gulpsync.sync([
          // 'vendor',
          "scripts:base",
          'scripts:app',
          'styles:app',
          'styles:min',
          'start'
        ]), function(){

  gutil.log(gutil.colors.cyan('************'));
  gutil.log(gutil.colors.cyan('* All Done *'), 'You can start editing your code, LiveReload will update your browser after any change..');
  gutil.log(gutil.colors.cyan('************'));

});

gulp.task('start',[
          'copy',
          'templates:app',
          'templates:views',
          'watch'
        ]);

gulp.task('done', function(){
  console.log('All Done!! You can start editing your code, LiveReload will update your browser after any change..');
});

// Error handler
function handleError(err) {
  console.log(err.toString());
  this.emit('end');
}

