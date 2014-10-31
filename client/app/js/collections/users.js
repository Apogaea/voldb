define(['underscore','backbone','./models/user'],function(_,Backbone,UserModel){
  var Users=Backbone.Collection.extend({
    model: UserModel
  });
  return Users;
});
