var app = app || {};

$(function(){
    "use-strict";

    var Shifts = Backbone.Collection.extend({
        model: app.Shift,
        comparator: "start_time"
    });

    app.Shifts = Shifts;
});
