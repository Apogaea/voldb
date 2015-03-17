/*global Backbone,define, utils, $, _ */

define([
'../../views/shiftGrid' //todo pull this into app?
],function(ShiftGrid){  
  var ShiftController=Backbone.View.extend({ //todo are views really needed? Could we use something else? Maybe make a controller out of a base view?
    ShiftGridView:ShiftGrid,
    children:{},
    container:$('#content'), //todo change this and make configurable    
    take_shift:function(shiftModel,options){
      options=options||{};
      var uid=options.uid||this.parent.user.id;
      //console.log(shiftModel.set('owner'),uid);
      console.log(shiftModel);
      window.sm=shiftModel;
      this.shifts.trigger('claim',shiftModel.id,uid);
      //this.superCollection
      //console.log('user '+ this.app.user.id+' is taking:',shiftModel);
    },//todo
    release_shift:function(shiftModel,options){
      
    },//todo
    edit_shift:function(shiftModel,options){},//todo
    initialize:function(options){
      console.log('creating shiftapp');
      _.extend(this,options);
    },
    destroy_grid:function(name){
      this.children[name].remove();
      //todo do we need to do anything else?
      
    },
    create_grid:function(options){
      console.log('making shiftgrid');
      //todo remove defaults
      //todo refactor object structure to extend cleanly
      options=options||{};
//
      //console.log('zzzz???zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',this.parent.collections.roles.get_roles_by_department(this.parent.collections.departments.get_id_by_name("Center Camp")))
      //options.filter = (options.filter||{"department":this.departments.get_id_by_name("Center Camp")});  
      options.name= options.name||"default test view";
      options.collection=options.collection||this.shifts.get_shifts(options);//todo pluck only required info
      options.controller=this;
      //todo handle name collisions      
      return utils.create_subview(options.name,this.ShiftGridView,options,this);
    },
    start:function(params){
      console.log('shiftApp.start')
      _.extend(this,params);
      if(this.parent&&this.parent.collections){
        this.roles=this.parent.collections.roles; //todo is there a better way to do this?
        this.departments=this.parent.collections.departments; //todo is there a better way to do this?
        this.shifts=this.parent.collections.shifts;
      }
      else{
        console.error('parent collections missing');
      }
      this.draw();//todo remove this, or at least make it configurable
      window.shiftApp=this;//todo remove this
      return this;
    },
    draw:function(){
     
     /*this.create_grid({
       "department":this.departments.get_id_by_name("ASS"),
       "name":"Another che"
     });
      window.sg=this.create_grid({
       "department":this.departments.get_id_by_name("Gate"),
       "name":"Another gate shiftgrid"
     });//this one is just debug*/
      console.log('drawing',this.config);
      this.container.html(this.create_grid(this.config).render().el);//todo create only if view not already instantiated
      
    },
    stop:function(){
      return this;
    }//todo cleanup gracefully
  });
  return ShiftController;
});
