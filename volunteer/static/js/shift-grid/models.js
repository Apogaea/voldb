var app = app || {};

$(function(){
    "use-strict";

    /*
     *  Models that are backed by database tables.
     */
    var Role = Backbone.Model.extend({
        initialize: function(options) {
            if ( _.isArray((options || {}).shifts) ) {
                var shifts = new app.Shifts(options.shifts);
                this.set("shifts", shifts);
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
            var claimedSlots = new app.Slots((options || {}).claimed_slots || []);
            this.set("claimed_slots", claimedSlots);
            this.listenTo(claimedSlots, "add remove", this.refetchShift);
        },
        refetchShift: function() {
            this.fetch();
        },
        parse: function(response, options) {
            this.get("claimed_slots").reset(response.claimed_slots || []);
            delete response.claimed_slots;
            return response;
        },
        urlRoot: "/api/v2/shifts/",
        url: function() {
            return this.urlRoot + this.id + "/";
        },
        isHydrated: function() {
            return Boolean(_.without(Object.keys(this.attributes), "id", "claimed_slots").length);
        },
        /*
         *  Claiming slots
         */
        claimUrl: function() {
            return this.url() + "claim/";
        },
        claimSlot: function(options) {
            return Backbone.sync("create", new app.Slot(), {
                url: this.claimUrl(),
                success: _.bind(this.cliamSlotSuccess, this)
            });
        },
        cliamSlotSuccess: function(slotData) {
            this.get("claimed_slots").add(slotData);
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "shiftIcon",
            "alreadyClaimedByUser",
            "hasOpenSlots",
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
        hasOpenSlots: function() {
            return Boolean(this.get("open_slot_count"));
        },
        alreadyClaimedByUser: function() {
            return !_.isUndefined(this.get("claimed_slots").findWhere({volunteer: window.django_user.id}));
        },
        isClaimable: function() {
            if ( this.get("is_locked") || !this.hasOpenSlots() ) {
                return false;
            } else if ( this.alreadyClaimedByUser() ) {
                return false;
            }
            return true;
        },
    });

    var Slot = Backbone.Model.extend({
        urlRoot: "/api/v2/slots/",
        url: function() {
            return this.urlRoot + this.id + "/";
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "isClaimedByUser",
        ],
        isClaimedByUser: function() {
            return this.get("volunteer") === window.django_user.id;
        }
    });

    /*
     *  Meta models that are used for the shift grid views
     */
    var GridCell = Backbone.Model.extend({
        initialize: function(options) {
            // Setup shift collection
            var shifts = new app.Shifts(_.map(options.shifts, function(shiftId) {
                return {id: shiftId};
            }));
            this.set("shifts", shifts);
            delete options.shifts;

            // Setup roles collection
            var roles = new app.Roles(options.roles);
            this.set("roles", roles);
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
            this.set("date", moment(options.date));
        }
    });

    var GridPageInfo = Backbone.Model.extend({
        defaults: {
            selectedDate: null
        },
        selectPage: function(pageNumber) {
            var dates = this.get("dates");
            var selectedPage = _.min([
                _.max([
                    Number(pageNumber) - 1,
                    0
                ]),
                this.totalPages() - 1
            ]);
            this.set("selectedDate", dates[selectedPage]);
        },
        /*
         *  Template and View Helpers
         */
        exportable: [
            "totalPages",
            "activePage",
            "hasPreviousPage",
            "hasNextPage",
            "pages",
        ],
        totalPages: function() {
            return this.get("dates").length;
        },
        activePage: function() {
            if ( _.isNull(this.get("selectedDate")) ) {
                return 1;
            } else {
                return _.indexOf(this.get("dates"), this.get("selectedDate")) + 1;
            }
        },
        hasPreviousPage: function() {
            return this.activePage() > 1;
        },
        hasNextPage: function() {
            return this.activePage() < this.totalPages();
        },
        pages: function() {
            var dates = this.get("dates");
            var activePage = this.activePage();
            return _.map(this.get("dates"), function(date) {
                var pageNumber = _.indexOf(dates, date) + 1;
                return {
                    pageNumber: pageNumber,
                    isActive: pageNumber === activePage,
                    dateDisplay: date.format("ddd (Do)")
                };
            });
        }
    });

    app.GridPageInfo = GridPageInfo;
    app.Role = Role;
    app.Shift = Shift;
    app.Slot = Slot;
    app.GridCell = GridCell;
    app.GridRow = GridRow;
});
