var app = app || {};

$(function(){
    "use-strict";

    var Shift = Backbone.Model.extend({
        urlRoot: "/api/v2/shifts/",
        url: function() {
            return this.urlRoot + this.id + "/";
        }
    });

    var GridCell = Backbone.Model.extend({
        initialize: function(options) {
            var shifts = new app.Shifts(_.map(options.shifts, function(shiftId) {
                return {
                    id: shiftId
                };
            }));
            shifts.each(function(shift) {
                shift.fetch();
            })
            this.set('shifts', shifts);

            delete options.shifts;

            this.set("end_time", new Date(options.end_time));
            delete options.end_time;

            this.set("start_time", new Date(options.start_time));
            delete options.start_time;
        }
    });

    app.Shift = Shift;
    app.GridCell = GridCell;
});
