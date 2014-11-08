define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    url:'./data/shifts.json',
    model: ShiftModel,
    initialize:function(){
      console.log('shift init');
      this.fetch();
    },
    parse:utils.parseCollection
  });
  return Shifts;
});
