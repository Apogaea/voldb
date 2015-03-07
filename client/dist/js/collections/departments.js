/*global define,utils */
define(['underscore','backbone','DepartmentModel'],function(_,Backbone,DepartmentModel){
  var Department=Backbone.Collection.extend({
    url:'http://localhost:8000/api/v2/departments/',
    model: DepartmentModel,
    initialize:function(){
      console.log('dept init');
      this.fetch({
        success:function(collection){
          collection.trigger('loaded');
        }
      });
    },
    get_name_by_id:function(id){//todo make this neater via BaseCollection
      return utils.get_name_by_id(id,this);
    }, 
    get_id_by_name:function(name){
      return utils.get_id_by_name(name,this);
    },
    get_id_by_role:function(){},
    parse:utils.parse_collection
  });
  return Department;
});
