var app = app || {};

$(function(){
    "use-strict";

    var GridCells = Backbone.Collection.extend({
        model: app.GridCell
    });

    var Shifts = Backbone.Collection.extend({
        model: app.Shift
    });

    var GridRows = Backbone.Collection.extend({
        model: app.GridRow
    });

    app.Shifts = Shifts;
    app.GridCells = GridCells;
    app.GridRows = GridRows;
});
