define([
  'jquery',
  'underscore',
  'backbone'
],function($,_,Backbone,UserCollection,ShiftCollection,DepartmentCollection){
  
  var Grid=Backbone.View.extend({
    initialize:function(){
      //console.log('making grid from',arguments,this);
      this.slots=[];
      _.each(this.collection,function(model){
        if(!this.slots[model.get('slot')]){
          this.slots[model.get('slot')]=[];
        }
        utils.splice_after(model,this.slots[model.get('slot')],'start_time');
      },this);
      console.log('slots are: ',this.slots);
    },
    render:function(){
      
    }
  });
  return Grid;
});
