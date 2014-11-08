define(['underscore','backbone','UserModel'],function(_,Backbone,UserModel){
  var Users=Backbone.Collection.extend({
    url:'./data/users.json',
    model: UserModel,
    initialize:function(){
      console.log('user init');
      this.fetch();
    },
    parse:utils.parseCollection
  });
  return Users;
});
