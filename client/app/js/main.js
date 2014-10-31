/*
 global require
*/
requirejs.config({
  shim: {
    backbone:{
      deps:['underscore','jquery'],
      exports:'Backbone'
    },
    router:{
      deps:['backbone']
    }
  },
  paths: {
    backbone:'./lib/backbone',
    underscore:'./lib/underscore',
    jquery:'./lib/jquery-1.11.1',
    appView: './views/app',
    router:'./router'
  }
});
require(['router']);
