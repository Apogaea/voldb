/*global define, utils 
* js/collections/shift.js
*/ 
define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    parse:utils.parse_collection,
    model: ShiftModel,
    children:[],
    initialize:function(models,options){
      if(options.url){
        this.url=options.url;
        if(options.fetch_on_init===true){
          this.fetch();
        }
      }
      //console.log('shift init');
      /*this.first_load=true;
      this.fetch({
        success:_.bind(function(collection) {
          this.trigger('update',collection);
          if(this.first_load){
            this.first_load=false;
            this.trigger('ready',collection);
          }
        }, this)
      });*/ 
    },
    get_shifts:function(attributes){ //todo add event to propagate changes/updates
      var subset,
          ChildCollection=Backbone.Collection.extend({//todo make this a utils method/mixin
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
      if(typeof attributes==='object'||attributes===undefined){
        if(typeof attributes==='object'){
          subset=new ChildCollection(this.where(attributes));
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
    }
  });
  return Shifts;
});
