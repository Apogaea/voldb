define(['underscore','backbone','./models/shift'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    model: ShiftModel
  });
  return Shifts;
});
