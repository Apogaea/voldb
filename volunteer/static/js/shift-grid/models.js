var app = app || {};

$(function(){
    "use-strict";

    var Shift = Backbone.Model.extend({
        urlRoot: "/api/v2/shifts/",
        url: function() {
            return this.urlRoot + this.id + "/";
        }
    });

    app.Shift = Shift;
});
