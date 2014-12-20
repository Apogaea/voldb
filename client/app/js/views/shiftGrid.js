/*global define, utils */
define([
  'jquery',
  'underscore',
  'backbone',
  'text!./templates/shiftItem.html'
],function($,_,Backbone,ShiftItem){  
  var Grid=Backbone.View.extend({
    shiftItem:_.template(ShiftItem),
    initialize:function(){
 
      //this.time_increment=30;//display grid in 30 minute increments
      this.slots=[];
      _.each(this.collection.models,function(model){
        if(!this.slots[model.get('slot')]){
          this.slots[model.get('slot')]=[];
        }
        utils.splice_after(model,this.slots[model.get('slot')],'start_time');
      },this);
      //this.render(this.slots);//take out of init
    },
    make_slot:function(shiftRow,bounds){
      //console.log('this row has:',shiftRow);
      //console.log(this.shiftItem);
      var slot=document.createElement('div');
      _.each(shiftRow,function(item){
        slot.innerHTML+=this.shiftItem({
          name:item.get('name'),
          length:(item.get('shift_length')*2)
        });
      },this);
      //console.log(slot);
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
      this.el.appendChild(frag);
      return this;
    }
  });
  return Grid;
});
