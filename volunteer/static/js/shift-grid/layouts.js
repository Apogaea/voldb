var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridLayout = Backbone.Marionette.LayoutView.extend({
        regions: {
            pagination: ".shift-grid-pagination",
            grid: ".shift-grid-table",
            cell_modal: ".cell-modal"
        }
    });

    app.ShiftGridLayout = ShiftGridLayout;
});
