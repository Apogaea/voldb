var app = app || {};

$(function(){
    "use-strict";
    var ShiftCellView = Backbone.Marionette.ItemView.extend({
    });

    var ShiftRowView = Backbone.Marionette.CompositeView.extend({
        childView: ShiftCellView
    });

    var ShiftGridView = Backbone.Marionette.CompositeView.extend({
        childView: ShiftRowView
    });

    app.ShiftGridView = ShiftGridView;
});


