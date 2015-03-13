var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridLayout = Backbone.Marionette.LayoutView.extend({
        regions: {
            grid: ".shift-grid",
            shift_modal: ".shift-modal",
        },
    });

    app.ShiftGridLayout = ShiftGridLayout;
});
