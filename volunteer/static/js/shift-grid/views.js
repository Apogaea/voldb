var app = app || {};

$(function(){
    "use-strict";
    var NestedCollectionCompositeView = Backbone.Marionette.CompositeView.extend({
        buildChildView: function(child, ChildViewClass, childViewOptions){
            // build the final list of options for the childView class
            if ( _.isUndefined(this.childCollectionProperty) ) {
                throw new Error("NestedCollectionCompositeViews must declare a childCollectionProperty");
            }
            var options = _.extend({
                model: child,
                collection: child.get(this.childCollectionProperty)
            }, childViewOptions);
            // create the child view instance
            var view = new ChildViewClass(options);
            // return it
            return view;
        },
    });

    var ShiftView = Backbone.Marionette.ItemView.extend({
        template: Handlebars.templates.shift_template
    });

    var ShiftCellView = Backbone.Marionette.CompositeView.extend({
        tagName: 'td',
        attributes: function() {
            var classes = [];
            if ( this.model.get("is_empty") ) { classes.push("empty"); }
            if ( this.model.get("open_on_left") ) { classes.push("open-left"); }
            if ( this.model.get("open_on_right") ) { classes.push("open-right"); }
            return {
                colspan: this.model.get("columns"),
                classes: classes.join(' ')
            };
        },
        childView: ShiftView,
        template: Handlebars.templates.shift_cell_template
    });

    var ShiftRowView = NestedCollectionCompositeView.extend({
        tagName: 'tr',
        childView: ShiftCellView,
        childCollectionProperty: "shifts",
        template: Handlebars.templates.shift_row_template
    });

    var ShiftGridView = NestedCollectionCompositeView.extend({
        tagName: 'table',
        attributes: {
            class: "table table-bordered shift-grid"
        },
        childView: ShiftRowView,
        childCollectionProperty: "cells",
        template: Handlebars.templates.shift_grid_template
    });

    app.ShiftGridView = ShiftGridView;
});
