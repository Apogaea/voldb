var app = app || {};

$(function(){
    "use-strict";

    var Roles = Backbone.Collection.extend({
        model: app.Role,
        url: "/api/v2/roles/"
    });

    var Shifts = Backbone.Collection.extend({
        model: app.Shift,
        url: "/api/v2/roles/"
    });

    var Slots = Backbone.Collection.extend({
        model: app.Slot,
        url: "/api/v2/slots/"
    });

    var GridCells = Backbone.Collection.extend({
        model: app.GridCell,
        getDenominators: function(value) {
            var denominators = [];
            for (var i = 0; i <= Math.floor(Math.sqrt(value)); i++) {
                if ( value % i === 0 ) {
                    denominators.push(i, value / i);
                }
            }
            return denominators;
        },
        columnDenominators: function() {
            return _.chain(this.pluck("columns"))
                .uniq()
                .map(this.getDenominators)
                .applyIntesection()
                .value();
        }
    });

    var GridRows = Backbone.Collection.extend({
        model: app.GridRow,
        comparator: function(a, b) {
            if ( a.get("date") < b.get("date") ) {
                return -1;
            } else if ( a.get("date") > b.get("date") ) {
                return 1;
            } else {
                return 0;
            }
        },
        getPageInfo: function() {
            return {
                dates: _.uniq(this.pluck('date'), true, function(date) {
                    return date.toString();
                })
            };
        }
    });

    app.Roles = Roles;
    app.Shifts = Shifts;
    app.Slots = Slots;
    app.GridCells = GridCells;
    app.GridRows = GridRows;
});
