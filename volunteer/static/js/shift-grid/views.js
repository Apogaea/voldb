var app = app || {};

$(function(){
    "use-strict";
    var SingleCellView = Backbone.Marionette.ItemView.extend({
    });

    var SingleRowView = Backbone.Marionette.CompositeView.extend({
        childView: ShiftCellView
    });

    var ShiftGridView = Backbone.Marionette.CompositeView.extend({
        childView: ShiftRowView
    });

    app.ShiftGridView = ShiftGridView;
});


