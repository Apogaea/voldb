/*global define, utils */
console.log(':)');
define([
'../../views/shiftGrid'
],function(ShiftGrid){  
var Controller=Backbone.View.extend({
  ShiftGridView:ShiftGrid,
  start:function(){
    console.log('starting');
  }
});
  
return Controller;
});
