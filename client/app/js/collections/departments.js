define(['underscore','backbone','DepartmentModel'],function(_,Backbone,DepartmentModel){
  var Department=Backbone.Collection.extend({
    url:'./data/departments.json',
    model: DepartmentModel,
    initialize:function(){
      console.log('dept init');
      this.fetch();
    },
    parse:utils.parseCollection
  });
  return Department;
});
