define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    url:'./data/shifts.json',
    model: ShiftModel,
    initialize:function(){
      //console.log('shift init');
      this.first_load=true;
      this.fetch({
        success:_.bind(function(collection) {
          console.log(this,arguments);
          this.trigger('update',collection);
          if(this.first_load){
            this.first_load=false;
            this.trigger('ready',collection);
          }
        }, this)
      });
      
    },
    get_shifts:function(attributes){
      if(typeof attributes==='object'){
        return this.where(attributes);
      }
      else if(attributes===undefined){
        return this.models;
      }
      else{
        return null;
      }
    },
    parse:utils.parse_collection
  });
  return Shifts;
});
