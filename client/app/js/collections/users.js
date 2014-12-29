define(['underscore','backbone','UserModel'],function(_,Backbone,UserModel){
  var Users=Backbone.Collection.extend({
    url:'./data/users.json',
    model: UserModel,
    initialize:function(){
      //console.log('user init');
      
      this.add({ //todo remove this after auth is set up 
        "id":10,
        "is_admin":true,
        "email":"rafe@bestdog.com",
        "user":"rafe",
        "full_name":"Rafe the Pirate King",
        "display_name":"Rafe",
        "phone":"",
        "has_ticket":false //no dogs allowed at apo :(
      });
    },
    fetch: function(options) {
      //todo update url based on options to augment request. 
      return Backbone.Collection.prototype.fetch.call(this, options);
    },
    get_current:function(){
      return this.get(10); //todo make this actually work after auth is set up.
    },
    parse:utils.parse_collection
  });
  return Users;
});
