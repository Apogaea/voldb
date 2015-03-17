/*global define, utils 
* js/collections/roles.js
*/ 
define(['underscore','backbone','RoleModel'],function(_,Backbone,RoleModel){
  var Roles=Backbone.Collection.extend({ //todo extend from custom collection which shims ChildCollection creation
    model: RoleModel,
    departments:{},
    children:[],
    register_events:function(){
      this.on('add',function(role){
        if(!this.departments[role.get('department')]){
          var ChildCollection=Backbone.Collection.extend({//todo make this a utils method/mixin
            model:RoleModel,//todo make this configurable
            parent:this,
            add: function(models,options) {
              this.parent.add(models, options);
              return Backbone.Collection.prototype.add.call(this,models, options);
            },
            remove: function(models,options) {
              this.parent.remove(models, options);
              return Backbone.Collection.prototype.remove.call(this,models, options);
            }            
          });          
          this.departments[role.get('department')]=new ChildCollection();
        }
        this.departments[role.get('department')].add(role);
        
      //  console.log(this.departments);
        
      },this);
    },
    initialize:function(models,options){
      //console.log('initing role collection');
      if(options.parent){this.parent=this;}
      if(options.url){
        this.url=options.url;
        if(options.fetch_on_init===true){
          //console.log('fetching roles from',this.url);
          this.fetch({
            success:function(collection){
              collection.trigger('loaded');
            }
          });
        }
      }
      this.register_events();
    },
    get_roles_by_department:function(departmentId){
      return this.departments[departmentId];
      
    },
    get_department_by_id:function(id){
     return this._byId[id];
    },
    get_roles:function(filter){ //todo add event to propagate changes/updates
      console.log('getting shifts',this,filter);
      var subset,
          ChildCollection=Backbone.Collection.extend({//todo make this a utils method/mixin
            model:RoleModel,//todo make this configurable
            parent:this,
            add: function(models,options) {
              this.parent.add(models, options);
              return Backbone.Collection.prototype.add.call(this,models, options);
            },
            remove: function(models,options) {
              this.parent.remove(models, options);
              return Backbone.Collection.prototype.remove.call(this,models, options);
            }            
          });
      if(typeof filter==='object'||filter===undefined){
        if(typeof filter==='object'){
          console.log(this,this.where(filter)); 
          subset=new ChildCollection(this.where(filter));
        }
        else{ //please don't use this often. It seems like a bad idea.
          subset=new ChildCollection(this.models);
        }
        this.children.push(subset);
        return subset;
      }
      else{
        return null;
      }
    },
    get_name_by_id:function(id){//todo make this neater via BaseCollection
      return utils.get_name_by_id(id,this);
    }, 
    get_id_by_name:function(name){
      return utils.get_id_by_name(name,this);
    },
    parse:utils.parse_collection
  });
  return Roles;
});
