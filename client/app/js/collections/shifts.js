define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    url:'./data/shifts.json',
    model: ShiftModel,
    initialize:function(){
      //console.log('shift init');
      this.first_load=true;
      this.fetch({
        success:_.bind(function(collection) {
          this.trigger('update',collection);
          if(this.first_load){
            this.first_load=false;
            this.trigger('ready',collection);
          }
        }, this)
      });
      
    },
    get_shifts:function(attributes){
      var Collection=Backbone.Collection.extend();
      if(typeof attributes==='object'){
        return new Collection(this.where(attributes));
      }
      else if(attributes===undefined){
        return new Collection(this.models);
      }
      else{
        return null;
      }
    },
    parse:utils.parse_collection
  });
  return Shifts;
});
