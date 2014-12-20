'use strict';

module.exports = function (grunt) {

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Configurable paths
  var config = {
    appLocation: 'app',
    distLocation: 'dist',
    servePort: 9000,
    testPort: 9001
  };

  // Define the configuration for all the tasks
  grunt.initConfig({

    // Project settings
    config: config,

    // Watches files for changes and runs tasks based on the changed files
    watch: {

      bower: {
        files: ['bower.json'],
        tasks: ['wiredep']
      },

      js: {
        files: ['<%= config.appLocation %>/js/**/*.js', '<%= config.appLocation %>/js/templates/**/*.html'],
        tasks: [ 
          //'jshint'
        ],
        options: {
          livereload: true
        }
      },

      jstest: {
        files: ['test/spec/{,*/}*.js'],
        tasks: ['test:watch']
      },

      gruntfile: {
        files: ['Gruntfile.js']
      },

      sass: {
        files: ['<%= config.appLocation %>/sass/{,*/}*.{scss,sass}'],
        tasks: ['sass:server', 'autoprefixer']
      },

      styles: {
        files: ['<%= config.appLocation %>/sass/{,*/}*.css'],
        tasks: ['newer:copy:styles', 'autoprefixer']
      },

      livereload: {
        options: {
          livereload: '<%= connect.options.livereload %>'
        },
        files: [
          '<%= config.appLocation %>/**/*.html',
          '.tmp/sass/**/*.css',
          '<%= config.appLocation %>/images/**/*'
        ]
      }
    },

    // The actual grunt server settings
    connect: {
      options: {
        port: '<%= config.servePort %>',
        open: true,
        livereload: 35729,
        // Change this to '0.0.0.0' to access the server from outside
        hostname: 'localhost'
      },
      livereload: {
        options: {
          middleware: function(connect) {
            return [
              connect.static('.tmp'),
              connect().use('/bower_components', connect.static('./bower_components')),
              connect.static(config.appLocation)
            ];
          }
        }
      },

      test: {
        options: {
          open: false,
          port: '<%= config.testPort %>',
          middleware: function(connect) {
            return [
              connect.static('.tmp'),
              connect.static('test'),
              connect().use('/bower_components', connect.static('./bower_components')),
              connect.static(config.appLocation)
            ];
          }
        }
      },
      dist: {
        options: {
          base: '<%= config.distLocation %>',
          livereload: false
        }
      }
    },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= config.distLocation %>/*',
            '!<%= config.distLocation %>/.git*'
          ]
        }]
      },
      server: '.tmp'
    },

    // Make sure code styles are up to par and there are no obvious mistakes
    jshint: {
      options: {
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      },
      all: [
        'Gruntfile.js',
        '<%= config.appLocation %>/js/{,*/}*.js',
        '!<%= config.appLocation %>/js/vendor/*',
        'test/spec/{,*/}*.js'
      ]
    },

    // Mocha testing framework configuration options
    mocha: {
      all: {
        options: {
          run: true,
          urls: ['http://<%= connect.test.options.hostname %>:<%= connect.test.options.port %>/index.html']
        }
      }
    },

    // Compile and optimize require modules
    requirejs: {
      compile: {
        options: {
          logLevel: 2,
          almond: true,
          name: '../../bower_components/almond/almond',
          baseUrl: '<%= config.appLocation %>/js',
          optimize: 'uglify',
          include: ['main.js'],
          out: "<%= config.distLocation %>/js/main.js",
          wrap: true,
          mainConfigFile: '<%= config.appLocation %>/require-config.js'
        }
      }
    },

    // Compiles Sass to CSS and generates necessary files if requested
    sass: {
      options: {
        // sourcemap: 'auto',
        loadPath: ['bower_components', 'bower_components/foundation/scss', '<%= config.appLocation %>/sass']
      },
      dist: {
        files: [{
          expand: true,
          cwd: '<%= config.appLocation %>/sass',
          src: ['*.{scss,sass}'],
          dest: '.tmp/sass',
          ext: '.css'
        }]
      },
      server: {
        files: [{
          src: ['<%= config.appLocation %>/sass/theme.scss'],
          dest: '.tmp/sass/main.css'
        }]
      }
    },

    // Add vendor prefixed styles
    autoprefixer: {
      options: {
        browsers: ['> 1%', 'last 2 versions', 'Firefox ESR', 'Opera 12.1']
      },
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/sass/',
          src: '{,*/}*.css',
          dest: '.tmp/sass/'
        }]
      }
    },

    // Automatically inject Bower components into the HTML file
    wiredep: {
      app: {
        ignorePath: /^\/|\.\.\//,
        src: ['<%= config.appLocation %>/index.html']
      },
      sass: {
        src: ['<%= config.appLocation %>/sass/{,*/}*.{scss,sass}'],
        ignorePath: /(\.\.\/){1,2}bower_components\//
      }
    },

    // Renames files for browser caching purposes
    rev: {
      dist: {
        files: {
          src: [
            '<%= config.distLocation %>/js/**/*.js',
            '<%= config.distLocation %>/sass/**/*.css',
            '<%= config.distLocation %>/images/**/*.*',
            '<%= config.distLocation %>/sass/fonts/**.*',
            '<%= config.distLocation %>/*.{ico,png}'
          ]
        }
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      options: {
        dest: '<%= config.distLocation %>'
      },
      html: '<%= config.appLocation %>/index.html'
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      options: {
        assetsDirs: [
          '<%= config.distLocation %>',
          '<%= config.distLocation %>/images',
          '<%= config.distLocation %>/sass'
        ]
      },
      html: ['<%= config.distLocation %>/{,*/}*.html'],
      css: ['<%= config.distLocation %>/sass/{,*/}*.css']
    },

    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= config.appLocation %>/images',
          src: '{,*/}*.{gif,jpeg,jpg,png}',
          dest: '<%= config.distLocation %>/images'
        }]
      }
    },

    svgmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= config.appLocation %>/images',
          src: '{,*/}*.svg',
          dest: '<%= config.distLocation %>/images'
        }]
      }
    },

    htmlmin: {
      dist: {
        options: {
          collapseBooleanAttributes: true,
          collapseWhitespace: true,
          conservativeCollapse: true,
          removeAttributeQuotes: true,
          removeCommentsFromCDATA: true,
          removeEmptyAttributes: true,
          removeOptionalTags: true,
          removeRedundantAttributes: true,
          useShortDoctype: true
        },
        files: [{
          expand: true,
          cwd: '<%= config.distLocation %>',
          src: '{,*/}*.html',
          dest: '<%= config.distLocation %>'
        }]
      }
    },

    // By default, your `index.html`'s <!-- Usemin block --> will take care
    // of minification. These next options are pre-configured if you do not
    // wish to use the Usemin blocks.
    // cssmin: {
    //   dist: {
    //     files: {
    //       '<%= config.distLocation %>/sass/main.css': [
    //         '.tmp/sass/{,*/}*.css',
    //         '<%= config.appLocation %>/sass/{,*/}*.css'
    //       ]
    //     }
    //   }
    // },
    // uglify: {
    //   dist: {
    //     files: {
    //       '<%= config.distLocation %>/js/scripts.js': [
    //         '<%= config.distLocation %>/js/scripts.js'
    //       ]
    //     }
    //   }
    // },
    concat: {
      dist: {}
    }, // Need to move back to usemin blocks

    // Copies remaining files to places other tasks can use
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= config.appLocation %>',
          dest: '<%= config.distLocation %>',
          src: [
            '*.{ico,png,txt}',
            'images/{,*/}*.webp',
            '{,*/}*.html',
            'styles/fonts/{,*/}*.*'
          ]
        }, {
          src: 'node_modules/apache-server-configs/dist/.htaccess',
          dest: '<%= config.distLocation %>/.htaccess'
        }]
      },
      styles: {
        expand: true,
        dot: true,
        cwd: '<%= config.appLocation %>/sass',
        dest: '.tmp/sass/',
        src: '{,*/}*.css'
      }
    },

    // Run some tasks in parallel to speed up build process
    concurrent: {
      server: [
        'sass:server',
        'copy:styles'
      ],
      test: [
        'copy:styles'
      ],
      dist: [
        'sass',
        'copy:styles',
        'imagemin',
        'svgmin'
      ]
    }

  }); // End initConfig

  grunt.registerTask('serve', 'start the server and preview your app, --allow-remote for remote access', function (target) {
    if (grunt.option('allow-remote')) {
      grunt.config.set('connect.options.hostname', '0.0.0.0');
    }
    if (target === 'dist') {
      return grunt.task.run(['build', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      'clean:server',
      // 'wiredep',
      'concurrent:server',
      'autoprefixer',
      'connect:livereload',
      'watch'
    ]);
  });

  grunt.registerTask('test', function (target) {
    if (target !== 'watch') {
      grunt.task.run([
        'clean:server',
        'concurrent:test',
        'autoprefixer'
      ]);
    }

    grunt.task.run([
      'connect:test',
      'mocha'
    ]);
  });

  grunt.registerTask('build', [
    'clean:dist',
    // 'wiredep',
    'useminPrepare',
    'concurrent:dist',
    'autoprefixer',
    'requirejs',
    'concat',
    'cssmin',
    // 'uglify',
    'copy:dist',
    'rev',
    'usemin',
    'htmlmin'
  ]);

  grunt.registerTask('default', [
    'newer:jshint',
    'test',
    'build'
  ]);
};
