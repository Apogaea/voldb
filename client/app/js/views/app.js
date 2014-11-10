define([
  'jquery',
  'underscore',
  'backbone',
  'UserCollection',
  'ShiftCollection',
  'DepartmentCollection',
  'ShiftGrid'
],function($,_,Backbone,UserCollection,ShiftCollection,DepartmentCollection,ShiftGrid){  
  var App=Backbone.View.extend({
    el:'#app',
    initialize:function(){ 
      this.collections={
        users:new UserCollection(),
        shifts:new ShiftCollection(),
        departments:new DepartmentCollection()
      };      
      console.log('gate shifts: ',this.collections.shifts.get_shifts());
      this.listenTo(this.collections.shifts,'ready',function(){//defer creating view until shifts are loaded
        this.views={
          gate:new ShiftGrid({
            collection:this.collections.shifts.get_shifts({department:'Gate'})
          })
        };
      });      
    }
  });
  return App;
});

