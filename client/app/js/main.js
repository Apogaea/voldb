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
  paths: {//these defines should all be single use.
    backbone:'./lib/backbone',
    underscore:'./lib/underscore',
    jquery:'./lib/jquery-1.11.1',
    text:'./lib/text',
    appView: './views/app',
    router:'./router',
    utils:'./utils',
    ShiftModel:'./models/shift',
    UserModel:'./models/user',
    RoleModel:'./models/role',
    DepartmentModel:'./models/department',
    ShiftCollection:'./collections/shifts',
    UserCollection:'./collections/users',
    RoleCollection:'./collections/roles',
    DepartmentCollection:'./collections/departments'
  }
});
console.log('derp');
require(['utils','router']);

