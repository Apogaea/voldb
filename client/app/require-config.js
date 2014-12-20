//- web/app/config.js
 
require.config({
 
  baseUrl: 'js',
 
  paths: {
    'jquery': '../../bower_components/jquery/dist/jquery',
    'modernizr': '../../bower_components/modernizr/modernizr',
    'backbone': '../../bower_components/backbone/backbone',
    'underscore': '../../bower_components/underscore/underscore',
    'marionette': '../../bower_components/marionette/lib/backbone.marionette',
    'foundation': '../../bower_components/foundation/js/foundation',
    'text': '../../bower_components/text/text',
    'vendor': '../../vendor_components',

    'appView': 'views/app',
    'router':'router',
    'utils':'utils',
    'ShiftModel':'models/shift',
    'UserModel':'models/user',
    'DepartmentModel':'models/department',
    'ShiftCollection':'collections/shifts',
    'UserCollection':'collections/users',
    'DepartmentCollection':'collections/departments',
    'ShiftGrid':'views/shiftGrid'
  }, 
  
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: [
        'underscore',
        'jquery'
      ],
      exports: 'Backbone'
    },
    marionette: {
      deps: ['backbone'],
      exports: 'Backbone.Marionette'
    },
    foundation: {
      deps: [
        'jquery',
        'modernizr'
      ],
      exports: 'Foundation'
    },
    modernizr: {
      exports: 'Modernizr'
    },
  },
});
 
require(['main'], function() {});