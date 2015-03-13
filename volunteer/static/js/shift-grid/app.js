var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridApplication = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.shiftData = _.map(options.shifts, function(row) {
                return new app.GridRow(row.grid, row);
            });
        }
    });

    app.ShiftGridApplication = ShiftGridApplication;
});
