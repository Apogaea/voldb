define(['backbone','appView'],function(Backbone,AppView){

  var AppRouter = Backbone.Router.extend({
    routes: {
      "*actions": "defaultRoute"
    }
  });
  
  AppRouter = new AppRouter;
  AppRouter.on('route:defaultRoute', function () {
    window.volDB=new AppView();
  });
  Backbone.history.start();
  return AppRouter;
});
