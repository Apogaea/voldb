define([
  'jquery',
  'underscore',
  'backbone',
  './collections/users',
  './collections/shifts',
  './collections/departments'
],function($,_,Backbone,UserCollection,ShiftCollection,DepartmentCollection){
  
  var App=Backbone.View.extend({
    el:'#app',
    initialize:function(){ 
      this.users=new UserCollection();
      this.shifts=new ShiftCollection();
      this.departments=new DepartmentCollection();
    }
  });

  return App;
});

