var app = app || {};

$(function(){
    "use-strict";

    var Shift = Backbone.Model.extend({
        urlRoot: "/api/v2/shifts/",
        url: function() {
            return this.urlRoot + this.id + "/";
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "shiftIcon",
            "isClaimable",
        ],
        shiftIcon: function() {
            if ( this.get("is_locked") ) {
                return "lock";
            } else if ( this.get("has_open_slots") ) {
                return "plus-sign";
            } else {
                return "minus-sign";
            }
        },
        isClaimable: function() {
            if ( this.get("is_locked") || !this.get("has_open_slots") ) {
                return false;
            }
            return true;
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

            this.set("end_time", moment(options.end_time));
            delete options.end_time;

            this.set("start_time", new moment(options.start_time));
            delete options.start_time;
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "cellTitle",
        ],
        cellTitle: function() {
            var startAt = this.get("start_time");
            var endAt = this.get("end_time");
            if ( startAt.format("A") === endAt.format("A") ) {
                return startAt.format("h:mm") + "-" + endAt.format("h:mm A");
            } else {
                return startAt.format("h:mm A") + "-" + endAt.format("h:mm A");
            }
        }
    });

    var GridRow = Backbone.Model.extend({
        initialize: function(options) {
            this.set("cells", new app.GridCells(options.cells));
            delete options.cells;
        }
    });

    app.Shift = Shift;
    app.GridCell = GridCell;
    app.GridRow = GridRow;
});
