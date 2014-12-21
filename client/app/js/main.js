/*
 global require
*/
requirejs.config({
  baseUrl: 'js',
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
    text:'./lib/text',
    appView: './views/app',
    router:'./router',
    utils:'./utils',
    ShiftModel:'./models/shift',
    UserModel:'./models/user',
    DepartmentModel:'./models/department',
    ShiftCollection:'./collections/shifts',
    UserCollection:'./collections/users',
    DepartmentCollection:'./collections/departments'//,
    //ShiftGrid:'./views/shiftGrid'//,
    //ShiftTemplate:'text!./templates/shiftItem.html'
  }
});
console.log('derp');
require(['utils','router']);

