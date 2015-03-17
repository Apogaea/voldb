/*global require, define, utils 
* app/js/views/app.js
*/
define([//todo clean up creation of supercollections; this define block is fugly
  'jquery',
  'underscore',
  'backbone',
  'UserCollection', 
//  'RoleCollection',
  'ShiftCollection',
  'DepartmentCollection',
  'text!./templates/layout.html'
],function($,_,Backbone,UserCollection/*,RoleCollection*/,ShiftCollection,DepartmentCollection,layout){  
  var App=Backbone.View.extend({ //todo does this need to be a view?
    el:'#app',
    template:_.template(layout),
    collections:{},
    modules:{},
    current_module:null,
    current_user:null,    
    initialize:function(){
      //todo require these in contained block
      var check_completion,loaded_collections=0,
          self=this;//ew
      //console.log('----------------getting departments----------------------');
      
      check_completion = function (){
        loaded_collections++;
        if(loaded_collections==2){
          self.collections.shifts=new ShiftCollection([],{
            url:'/api/v2/shifts/', //todo request less stuff?
            fetch_on_init:true,
            parent:self
          });
          self.collections.shifts.once('ready',function(){
            self.collections.shifts.once('ready',self.trigger('ready'));
          });
          
        }
      };
      
      this.collections.departments=new DepartmentCollection([],{parent:this});
      this.collections.departments.once('loaded',check_completion);

      //this.collections.roles=new RoleCollection([],{
      //  url:'/api/v2/roles/', //todo remove this and give to controllers
      //  fetch_on_init:true,
      //  parent:this
      //});
//      this.collections.roles.once('loaded',check_completion);
      this.collections.users=new UserCollection();
      

      //todo remove these when optimizing. These are for ease of use while developing so you don't need to manually load modules.
      this.load_module('shift');
      this.load_module('search');
      this.load_module('landing');
      
      

      return this;
      
    },
    set_user:function(){//todo authentication
      this.user=this.collections.users.get_current(); //todo make this work; currently returns static uid for testing;  
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
      //console.log('loading '+path);
      options=options?options:{};
      options.app=this;
      if(this.modules[module]==undefined){
        //console.log('loading...');
        scope=this;//todo find a workaround. i hate doing this.
        require([path],function(Module){
//          console.log(this,scope)
          scope.modules[module]=new Module(options);
          scope.modules[module].parent=scope;
          if(cb){
            cb(scope.modules[module]);
          }
        });
      }
      else{
        cb(this.modules[module]);
        //todo loading/unloading existing
      }
    },
    start:function(module_name,params){
      this.set_user();//todo call this on auth
      console.log(module_name +' app starting');
      this.$el.html(this.template({
        title:'hello apo!'
      }));
      module_name=module_name||'landing';
      this.on('ready',function(){
       console.log('app ready');
        this.load_module(module_name,undefined,function(module){
          console.log(module_name+' module starting');
          module.start(params);
        });    
      },this);
    }
  });
  
  return App;
});

