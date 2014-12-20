define(['backbone','appView'],function(Backbone,AppView){

  var AppRouter = Backbone.Router.extend({
    routes: {
      "*actions": "defaultRoute",
      "user/:id": "viewUser"
    }
  });
  
  AppRouter = new AppRouter;
  AppRouter.on('route:defaultRoute', function () {
    if(!window.volDB){
        window.volDB=new AppView();
    } 
  });
  AppRouter.on('route:viewUser', function () {
    console.log('hi there user');
  });
  Backbone.history.start();
  return AppRouter;
});
