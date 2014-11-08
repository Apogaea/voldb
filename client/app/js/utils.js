define(['jquery','underscore'],function($,_){
  _.extend((window.utils=window.utils||{}),{
    parseCollection:function(data,options){
      //console.log(this,'parsing',arguments);
      return data.data?data.data:data;
    }
  });  
});
