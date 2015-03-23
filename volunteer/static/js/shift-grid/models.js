var app = app || {};

$(function(){
    "use-strict";

    var Role = Backbone.Model.extend({
        initialize: function(options) {
            if ( _.isArray(options.shifts) ) {
                var shifts = new app.Shifts(options.shifts);
                this.set('shifts', shifts);
                delete options.shifts;
            }
        },
        urlRoot: "/api/v2/roles/",
        url: function() {
            return this.urlRoot + this.id + "/";
        },
        isHydrated: function() {
            return Boolean(_.without(Object.keys(this.attributes), "id", "shifts").length);
        }
    });

    var Shift = Backbone.Model.extend({
        initialize: function(options) {
            this.set("claimed_slots", new app.Slots(options.claimed_slots || []));
        },
        parse: function(response, options) {
            this.get("claimed_slots").reset(response.claimed_slots || []);
            delete response.claimed_slots
            return response
        },
        urlRoot: "/api/v2/shifts/",
        url: function() {
            return this.urlRoot + this.id + "/";
        },
        isHydrated: function() {
            return Boolean(_.without(Object.keys(this.attributes), "id", "claimed_slots").length);
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
            } else if ( this.get("open_slot_count") ) {
                return "plus-sign";
            } else {
                return "minus-sign";
            }
        },
        isClaimable: function() {
            if ( this.get("is_locked") || !this.get("open_slot_count") ) {
                return false;
            }
            return true;
        },
    });

    var Slot = Backbone.Model.extend({
        urlRoot: "/api/v2/slots/",
        url: function() {
            return this.urlRoot + this.id + "/";
        }
    });

    var GridCell = Backbone.Model.extend({
        initialize: function(options) {
            // Setup shift collection
            var shifts = new app.Shifts(_.map(options.shifts, function(shiftId) {
                return {id: shiftId};
            }));
            this.set('shifts', shifts);
            delete options.shifts;

            // Setup roles collection
            var roles = new app.Roles(options.roles);
            this.set('roles', roles);
            delete options.roles;

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

    app.Role = Role;
    app.Shift = Shift;
    app.Slot = Slot;
    app.GridCell = GridCell;
    app.GridRow = GridRow;
});
