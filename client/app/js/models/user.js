define(['underscore','backbone'],function(_,Backbone){
  console.log('creating user model');
  var User=Backbone.Model.extend({
    initialize:function(){
      //console.log('user model created',this,arguments);
    }
  });
  window.UserModel=User;
  return User;
});
