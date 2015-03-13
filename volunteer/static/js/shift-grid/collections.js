var app = app || {};

$(function(){
    "use-strict";

    var GridRow = Backbone.Collection.extend({
        model: app.GridCell,
        comparator: "start_time",
        initialize: function(models, options) {
            this.shiftLength = options.length;
            this.gridDate = options.date;
        }
    });

    var Shifts = Backbone.Collection.extend({
        model: app.Shift
    });

    app.Shifts = Shifts;
    app.GridRow = GridRow;
});
