/*global define, utils 
* app/js/views/app.js
*/
define([
  'jquery',
  'underscore',
  'backbone',
  'UserCollection',
  'ShiftCollection',
  'DepartmentCollection',
  'text!./templates/layout.html'
],function($,_,Backbone,UserCollection,ShiftCollection,DepartmentCollection,layout){  
  var App=Backbone.View.extend({ //todo does this need to be a view?
    el:'#app',
    template:_.template(layout),
    collections:{},
    modules:{},
    current_module:null,
    initialize:function(){
      //todo require these in contained block
      this.collections.users=new UserCollection();
      this.collections.shifts=new ShiftCollection([],{
        url:'./data/shifts.json', //todo remove this and give to controllers
        fetch_on_init:true
      });
      this.collections.departments=new DepartmentCollection();
    
      
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
    },
    load_module:function(module,options,cb){
      var scope,
          path='./apps/'+module+'/'+module+'App';
      console.log('loading '+path);
      if(this.modules[module]==undefined){
        console.log('loading...');
        scope=this;//todo find a workaround. i hate doing this.
        require([path],function(Module){
          console.log(this,scope)
          scope.modules[module]=new Module({initialize:function(){
            
            utils.create_subview('gateGrid',scope.ShiftGridView,{
              collection:scope.collections.shifts.get_shifts({department:'Gate'})
            },scope);
            
          }});
          if(cb){
            cb(scope.modules[module]);
          }
        });
      }
      else{
        //todo loading/unloading existing
      }
    },
    start:function(module){
      console.log('app starting');
      module=module||'shift';
      this.load_module(module,undefined,function(module){
        console.log('module '+module+' starting');
        module.start();
      });    
    }
  });
  
  return App;
});

