/*global $,_,Backbone,define, utils */
define([
  'text!../templates/shiftGrid.html',
  'text!../templates/shiftItem.html'
],function(ShiftGrid,ShiftItem){  
  //console.log('hi',Backbone)
  var Grid=Backbone.View.extend({
    events:{
      "click .actions a":'handleAction'
    },
    handleAction:function(e){
      console.log('handleAction',e);
      var shiftItem=e.target,
          shiftId=$(e.target).parents("[shift]").first().attr('shift');//todo fix jquery abuse
      
      /*
       actions can be:
       - take
       - release
       - edit //todo after take/release is working
       */
      switch(shiftItem.hash){//todo refactor this mess
        case '#take':
        this.controller.take_shift(this.collection._byId[shiftId]);
        break;
        case '#release':
        this.controller.release_shift(this.collection._byId[shiftId]);
        break;
        default:
        console.log('wat');//todo
        break;
      }
      
    },
    template:_.template(ShiftGrid),
    shiftItem:_.template(ShiftItem),
    initialize:function(options){
      window.shiftGrid=this;//todo remove this
      _.extend(this,options);
      this.time_increment=30;//todo refactor configuration flow //display grid in 30 minute increments. 
      this.slots=[];
      
      if(this.collection&&this.collection.models){
       _.each(this.collection.models,function(model){
         if(model.get('slot')==undefined){
           model.set('slot',0);
         }
         //console.log(model.get('slot'));
         if(this.slots[model.get('slot')]==undefined){
           this.slots[model.get('slot')]=[];
         }
         utils.splice_after(model,this.slots[model.get('slot')],'start_time');
         //console.log(model,this.slots,model);
      },this);
      }
      //this.render(this.slots);//take out of init
    },
    make_slot:function(shiftRow,bounds){
      //console.log('this row has:',shiftRow);
      //console.log(this.shiftItem);
      var slot=document.createElement('div');
      _.each(shiftRow,function(item){
        slot.innerHTML+=this.shiftItem({
          shiftId:item.get('id'),
          name:this.controller.roles.get_name_by_id(item.get('role')),
          length:(item.get('shift_length')*20),//todo add percentage maths here
          start_time:utils.format_time(item.get('start_time'))
        });
      },this);
      return slot;
    },
    get_bounds:function(slots){
      var i,
          bounds={
            beginning:undefined,
            end:undefined
          };
      _.each(slots,function(slot){
        //console.log(slot);
        var end_time;
        if(slot!==undefined){
          if(bounds.beginning===undefined || 
             bounds.beginning>slot[0].get('start_time')){
            bounds.beginning=slot[0].get('start_time');
          }
          end_time=utils.get_end_time(slot[slot.length-1].get('start_time'),slot[slot.length-1].get('shift_length'));
          if(bounds.end===undefined || 
             bounds.end<end_time){
            bounds.end=end_time;
          }
        }
      });
      return bounds;
      
    },
    get_dimensions:function(bounds,parent){
      //console.log(bounds);
      //      console.log('getting parent dimensions',parent.$el.width());
    },
    render:function(slots){
      console.log('shiftGrid.render');
      slots=slots||this.slots;
      //console.log(this);
      //console.log(this.parent);
      var i,
          frag=document.createDocumentFragment(),
          bounds=this.get_bounds(slots),
          dimensions=this.get_dimensions(bounds,this.parent);
      for(i=0;i<slots.length;i++){
        if(slots[i]!==undefined){
          frag.appendChild(this.make_slot(slots[i],bounds));
        }
      }
      console.log(this);
      this.$el.html(this.template({
        name:'this is some test grid'
      })).append(frag);
      return this;
    }
  });
  return Grid;
});
