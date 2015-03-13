var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridApplication = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.shiftData = new app.GridRows(options.rows);
            this.shiftLayout = this.initializeLayout(options.el);
            this.shiftLayout.grid.show(new app.ShiftGridView({
                collection: this.shiftData
            }));
        },
        initializeLayout: function(el) {
            return new app.ShiftGridLayout({
                application: this,
                el: el
            });
        },
    });

    app.ShiftGridApplication = ShiftGridApplication;
});
