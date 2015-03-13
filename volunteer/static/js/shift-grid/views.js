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
        tagName: 'li',
        template: Handlebars.templates.shift_cell_template,
        modelEvents: {
            'sync': 'render'
        }
    });

    var GridCellView = Backbone.Marionette.CompositeView.extend({
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
        childViewContainer: 'ul.shifts',
        template: Handlebars.templates.grid_cell_template,
        templateHelpers: function() {
            return {
                x: 3  // TODO?
            };
        },
    });

    var ModalShiftView = Backbone.Marionette.ItemView.extend({
        triggers: {
            "click": "shift:click"
        },
        template: Handlebars.templates.shift_modal_template
    });

    var ModalCellView = Backbone.Marionette.CompositeView.extend({
        attributes: {
            class: "modal fade"
        },
        childView: ModalShiftView,
        childViewContainer: '.shifts',
        template: Handlebars.templates.cell_modal_template
    });

    var GridRowView = NestedCollectionCompositeView.extend({
        tagName: 'tr',
        childView: GridCellView,
        childCollectionProperty: "shifts",
        childEvents: {
            'cell:click': 'delegateClick'
        },
        delegateClick: function(cellView) {
            this.trigger("cell:click", cellView);
        },
        template: Handlebars.templates.grid_row_template
    });

    var GridView = NestedCollectionCompositeView.extend({
        tagName: 'table',
        attributes: {
            class: "table table-bordered shift-grid"
        },
        childView: GridRowView,
        childCollectionProperty: "cells",
        childEvents: {
            'cell:click': 'delegateClick'
        },
        delegateClick: function(childView, cellView) {
            this.trigger("cell:click", cellView);
        },
        template: Handlebars.templates.shift_grid_template
    });

    app.GridView = GridView;
    app.ModalCellView = ModalCellView;
});
