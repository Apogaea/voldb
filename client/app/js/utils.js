/*global define */
define(['jquery','underscore'],function($,_){
  _.extend((window.utils=window.utils||{}),{
    parse_collection:function(data,options){
      //console.log('parsing collection ',(data.results?data.results:data));
      return data.results?data.results:data;//todo handle pagination and error path 
    },
    splice_after:function(item,target,attribute){
      var i=0;
      if(target.length===0){
        target.push(item);
      }
      else{
        for(;i<target.length;i++){
          if(item.get(attribute)>target[i].get(attribute)||
             target[i][attribute]===undefined){
            target.splice(i+1,0,item);
            break;
          }
        }
      }
    },
    get_end_time:function(start,duration){
      var end_time=start;//todo refactor  into utility method
      end_time.setMinutes(end_time.getMinutes()+duration);
      return end_time;      
    },
    create_subview:function(name,SubView,options,scope){
      var child={};
      scope=scope||this;
      options=options||{};
      child[name]=new SubView(options);
      child[name].parent=scope;
      _.extend((scope.children=scope.children||{}),child);
      return child[name];
    }
  });  
});
