/*global Backbone,define, utils */

define([
'../../views/shiftGrid' //todo pull this into app?
],function(ShiftGrid){  
  var ShiftController=Backbone.View.extend({ //todo are views really needed? Could we use something else?
    ShiftGridView:ShiftGrid,
    children:{},
    take_shift:function(){},//todo
    release_shift:function(){},//todo
    edit_shift:function(){},//todo
    destroy_grid:function(name){
      this.children[name].remove();
      //todo do we need to do anything else?
    },
    create_grid:function(options){
      //console.log('making shiftgrid');
      //todo remove defaults
      //todo refactor object structure to extend cleanly
      options=options||{};
      options.filter = (options.filter||{"department":this.departments.get_id_by_name("Gate")}); 
      options.name= options.name||"default test view";
      options.collection=options.collection||this.superCollection.get_shifts(options.filter);
      options.controller=this;
      //todo handle name collisions      
      return utils.create_subview(options.name,this.ShiftGridView,options,this);
    },
    start:function(params){
      if(this.parent&&this.parent.collections){
        this.departments=this.parent.collections.departments; //todo is there a better way to do this?
        this.superCollection=this.parent.collections.shifts;
      }
      else{
        console.error('parent collections missing');
      }
      console.log(this.create_grid().render().el); //todo remove
      return this;
    },
    stop:function(){
      return this;
    }//todo
  });
  return ShiftController;
});
