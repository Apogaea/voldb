define(['underscore','backbone'],function(_,Backbone){
  var Shift=Backbone.Model.extend({
    initialize:function(){
      if(this.get('start_time')){
        this.set('start_time',new Date(this.get('start_time')));
      }
    }
  });
  return Shift;
});
