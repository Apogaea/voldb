/*global define, utils */
define([
  'jquery',
  'underscore',
  'backbone',
  'UserCollection',
  'ShiftCollection',
  'DepartmentCollection',
  'ShiftGrid',
  'text!./templates/layout.html'
],function($,_,Backbone,UserCollection,ShiftCollection,DepartmentCollection,ShiftGrid,layout){  
  var App=Backbone.View.extend({
    el:'#app',
    template:_.template(layout),
    initialize:function(){ 
      this.collections={
        users:new UserCollection(),
        shifts:new ShiftCollection([],{url:'./data/shifts.json',fetch_on_init:true}),
        departments:new DepartmentCollection()
      };      
/*      this.listenTo(this.collections.shifts,'ready',function(){//defer creating view until shifts are loaded
        utils.create_subview('gate',ShiftGrid,{
          collection:this.collections.shifts.get_shifts({department:'Gate'})
        },this);
        utils.create_subview('ass',ShiftGrid,{
          collection:this.collections.shifts.get_shifts({department:'ASS'})
        },this);
        this.render().render(['gate','ass']); //render without arguments loads bare layout. With args, it will render listed subviews
      });    */  
    },
    render:function(subviews,to_empty){
      //console.log(this.el);
      /*if(to_empty ){//todo make this not ugly
        this.$el.html(this.template({title:"hello apo."}));
      }*/

      if(subviews){
        var frag=document.createDocumentFragment();
        _.each(subviews,function(subview){
          frag.appendChild(this.children[subview].render().el);
        },this);
        this.$el.append(frag);
      }
      return this;
    }
  });
  
  return App;
});

