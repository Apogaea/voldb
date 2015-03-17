/*global define, utils 
* js/collections/shift.js
*/ 
define(['underscore','backbone','ShiftModel'],function(_,Backbone,ShiftModel){
  var Shifts=Backbone.Collection.extend({
    parse:utils.parse_collection,
    model: ShiftModel,
    roles:{},
    children:[],
    register_events:function(cb,scope){
      this.on('claim',function(shiftId,user){
        console.log('user '+user+' is claiming the shift with an id of '+shiftId);
        
        this._byId[shiftId].set('owner',user);
        this.sync('update',this._byId[shiftId],{type:"POST"});
        
      });
      this.on('release',function(shiftId,user){
        console.log('user '+user+' is releasing the shift with an id of '+shiftId);
        this._byId[shiftId].set('owner',null);        
        this.sync('update',this._byId[shiftId],{type:"POST"});
        
      });
      this.on('add',function(shift){
//        console.log('adding shift',shift);
        //utils.get_end_time(shift.get('start_time'),shift.get('duration'));
        shift.set('end_time',utils.get_end_time(shift.get('start_time'),shift.get('shift_length')));
        if(this.parent.collections.roles._byId[shift.get('role')]){//shim in department so we can query shifts by department quickly           
           shift.set('department',this.parent.collections.roles._byId[shift.get('role')].get('department'));
        }
        //shift.set('end_date')
        //console.log(this.parent.collections.roles._byId[]);
        if(!this.roles[shift.get('role')]){
          var ChildCollection=Backbone.Collection.extend({//todo make this a utils method/mixin
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
          this.roles[shift.get('role')]=new ChildCollection();
        }
        this.roles[shift.get('role')].add(shift);
        //console.log(this.roles);
      },this);
      cb.call(scope);
    },
    initialize:function(models,options){
      console.log('initing shift collection',options);
      if(options.parent){
        //console.log('setting parent:',options.parent);
        this.parent=options.parent;
      }
      this.register_events(function(){
        if(options.url){
          this.url=this.defaultUrl=options.url;
          if(options.fetch_on_init===true){
            //console.log('fetching shifts from',this.url);
            this.fetch_all_shifts();
          }
        }
      },this);//todo make this pubsubbable
      
      
      
    },
    fetch_all_shifts:function(url){
      //console.log(this);
      var self=this;
      if(!url){
        this.url=this.defaultUrl;
      }
      else{
        this.url=url;
      }
      this.fetch({remove:false,complete:function(xhr,status){
       // console.log(arguments);
        if(status!=='success'){
          //todo retry
        }
        else if(xhr.responseJSON.next){
          //console.log('fetching next page',xhr.responseJSON);
          self.fetch_all_shifts(xhr.responseJSON.next);
        }
        else{                  
          //console.log('done with pagination',xhr.responseJSON);
          console.log(self.trigger('ready'));
        }
      }});
    },
    get_shifts:function(params){
      params=params||{};
      //todo add event to propagate changes/updates
      //console.log('getting shifts',this,filter);
      var subset=this,
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
      
      if(typeof params.where==='object'){
       // console.log(subset,subset.where(params.where));
        subset=new ChildCollection(subset.where(params.where));
      }
      if(typeof params.filter==='function'){
        console.log(subset,subset.where(params.filter));
        subset=new ChildCollection(subset.filter(params.filter));
      }
      if(typeof params.date_range==='object'){
        console.log(subset,subset.where(params.filter));
        subset=new ChildCollection(subset.filter(function(model){
          return (model.get('start_time')>=params.date_range.start_time&&model.get('end_time')<=params.date_range.end_time);
        }));
      }      
      this.children.push(subset);
      return subset;
      
    }
  });
  return Shifts;
});
