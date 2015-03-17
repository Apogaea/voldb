/*global Backbone,define, utils, $, _ */

define([
'../../views/landing' //todo pull this into app?
],function(LandingView){  
  var LandingController=Backbone.View.extend({ //todo are views really needed? Could we use something else? Maybe make a controller out of a base view?
    landingView:LandingView,
    children:{},
    container:$('#content'), //todo change this and make configurable    
    initialize:function(options){
      console.log('creating landingapp');
      _.extend(this,options);
    },
    start:function(params){
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
      //this.container.html(this.create_grid().render().el);//todo create only if view not already instantiated
    },
    stop:function(){
      return this;
    }//todo cleanup gracefully
  });
  return LandingController;
});
