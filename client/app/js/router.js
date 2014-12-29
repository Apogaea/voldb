define(['backbone','appView'],function(Backbone,AppView){
  
  var AppRouter = Backbone.Router.extend({
    routes: {
      "*actions": "defaultRoute",
      "user/:id": "viewUser"
    }
  }),
      volDB;
  
  AppRouter = new AppRouter;
  AppRouter.on('route:defaultRoute', function () {
    if(!volDB){
      volDB=new AppView();
      volDB.start('shift');
      window.volDB=volDB;//todo remove this for prod 
    } 
  });
  AppRouter.on('route:viewUser', function () {
    console.log('hi there user');
  });
  Backbone.history.start();
  return AppRouter;
});
