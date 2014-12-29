/*global define, utils 
* js/collections/shift.js
*/ 
define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    parse:utils.parse_collection,
    model: ShiftModel,
    children:[],
    initialize:function(models,options){
      console.log('initing shift collection');
      if(options.url){
        this.url=options.url;
        if(options.fetch_on_init===true){
          console.log('fetching shifts from',this.url);
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
    get_shifts:function(filter){ //todo add event to propagate changes/updates
      console.log('getting shifts',this,filter);
      var subset,
          ChildCollection=Backbone.Collection.extend({//todo make this a utils method/mixin
            model:ShiftModel,//todo make this configurable
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
    }
  });
  return Shifts;
});
