define(['underscore','backbone','UserModel'],function(_,Backbone,UserModel){
  var Users=Backbone.Collection.extend({
    url:'./data/users.json',
    model: UserModel,
    initialize:function(){
      //console.log('user init');
      //this.fetch();//nope, this is dumb
    },
    fetch: function(options) {
      //todo update url based on options to augment request. 
      return Backbone.Collection.prototype.fetch.call(this, options);
    },
    parse:utils.parse_collection
  });
  return Users;
});
