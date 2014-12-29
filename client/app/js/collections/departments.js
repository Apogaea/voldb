define(['underscore','backbone','DepartmentModel'],function(_,Backbone,DepartmentModel){
  var Department=Backbone.Collection.extend({
    url:'./data/departments.json',
    model: DepartmentModel,
    initialize:function(){
      //console.log('dept init');
      this.fetch();
    },
    get_name_by_id:function(id){//todo make mixin
      var result=this.findWhere({id:id});
      if(result!==undefined){
        return result.get('name');
      }
      else{
        return null;
      }
    },
    get_id_by_name:function(name){ //todo make mixin
      var result=this.findWhere({name:name});
      if(result!==undefined){
        return result.get('id');
      }
      else{
        return null;
      }
    },
    parse:utils.parse_collection
  });
  return Department;
});
