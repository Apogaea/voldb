/*global define,utils */
define(['underscore','backbone','DepartmentModel'],function(_,Backbone,DepartmentModel){
  var Department=Backbone.Collection.extend({
    url:'./data/departments.json',
    model: DepartmentModel,
    initialize:function(){
      //console.log('dept init');
      this.fetch();
    },
    get_name_by_id:function(id){//todo make this neater via BaseCollection
      return utils.get_name_by_id(id,this);
    }, 
    get_id_by_name:function(name){
      return utils.get_id_by_name(name,this);
    },
    parse:utils.parse_collection
  });
  return Department;
});
