define(['underscore','backbone'],function(_,Backbone){
  var Shift=Backbone.Model.extend({
    initialize:function(){
      if(this.id){
        this.url='/api/v2/shifts/:'+this.id;
      }
      else{
        console.log('no url?',this.url);
      }
      //console.log('making shift model',this,arguments);
      if(this.get('start_time')){
        //console.log('converting time object');
        this.set('start_time',new Date(this.get('start_time')));
      }
    }
  });
  return Shift;
});
