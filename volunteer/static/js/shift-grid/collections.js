var app = app || {};

$(function(){
    "use-strict";

    var Roles = Backbone.Collection.extend({
        model: app.Role,
        url: "/api/v2/roles/"
    });

    var Shifts = Backbone.Collection.extend({
        model: app.Shift,
        url: "/api/v2/roles/"
    });

    var Slots = Backbone.Collection.extend({
        model: app.Slot,
        url: "/api/v2/slots/"
    });

    var GridCells = Backbone.Collection.extend({
        model: app.GridCell
    });

    var GridRows = Backbone.Collection.extend({
        model: app.GridRow
    });

    app.Roles = Roles;
    app.Shifts = Shifts;
    app.Slots = Slots;
    app.GridCells = GridCells;
    app.GridRows = GridRows;
});
