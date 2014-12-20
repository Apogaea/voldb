define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    url:'./data/shifts.json',
    model: ShiftModel,
    children:[],
    initialize:function(){
      //console.log('shift init');
      this.first_load=true;
      this.fetch({
        success:_.bind(function(collection) {
          this.trigger('update',collection);
          if(this.first_load){
            this.first_load=false;
            this.trigger('ready',collection);
          }
        }, this)
      }); 
    },
    add: function(models,options) {
      //trigger event to update children
      return Backbone.Collection.prototype.add.call(this,models, options);
    },
    get_shifts:function(attributes){ //todo add event to propagate changes/updates
      var subset,
          ChildCollection=Backbone.Collection.extend({
            parent:this,
            add: function(models,options) {
              this.parent.add(models, options);
              return Backbone.Collection.prototype.add.call(this,models, options);
            }
          });
      if(typeof attributes==='object'||attributes===undefined){
        if(typeof attributes==='object'){
          subset=new ChildCollection(this.where(attributes));
        }
        else{ //please don't use this often. It seems like a really bad idea.
          subset=new ChildCollection(this.models);
        }
        this.children.push(subset);
        return subset;
      }
      else{
        return null;
      }
    },
    parse:utils.parse_collection
  });
  return Shifts;
});
