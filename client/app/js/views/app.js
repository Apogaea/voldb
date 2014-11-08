define([
  'jquery',
  'underscore',
  'backbone',
  'UserCollection',
  'ShiftCollection',
  'DepartmentCollection'
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

