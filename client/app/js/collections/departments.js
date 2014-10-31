define(['underscore','backbone','./models/department'],function(_,Backbone,DepartmentModel){
  var Departments=Backbone.Collection.extend({
    model: DepartmentModel
  });
  return Departments;
});
