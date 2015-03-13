var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridLayout = Backbone.Marionette.LayoutView.extend({
        regions: {
            grid: ".shift-grid",
            cell_modal: ".cell-modal",
        },
    });

    app.ShiftGridLayout = ShiftGridLayout;
});
