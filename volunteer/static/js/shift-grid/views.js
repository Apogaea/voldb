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

    var GridCellView = Backbone.Marionette.ItemView.extend({
        tagName: "td",
        attributes: function() {
            var classes = [];
            if ( this.model.get("is_empty") ) { classes.push("empty"); }
            if ( this.model.get("open_on_left") ) { classes.push("open-left"); }
            if ( this.model.get("open_on_right") ) { classes.push("open-right"); }
            return {
                colspan: this.model.get("columns"),
                classes: classes.join(" ")
            };
        },
        triggers: {
            "click": "cell:click"
        },
        template: Handlebars.templates.grid_cell_template
    });

    var GridRowView = NestedCollectionCompositeView.extend({
        tagName: "tr",
        childView: GridCellView,
        childCollectionProperty: "shifts",
        childEvents: {
            "cell:click": function(cellView) {
                this.trigger("cell:click", cellView);
            }
        },
        template: Handlebars.templates.grid_row_template
    });

    var GridView = NestedCollectionCompositeView.extend({
        tagName: "table",
        attributes: {
            class: "table table-bordered shift-grid"
        },
        childView: GridRowView,
        childCollectionProperty: "cells",
        childEvents: {
            "cell:click": function(childView, cellView) {
                this.trigger("cell:click", cellView);
            }
        },
        template: Handlebars.templates.shift_grid_template
    });

    /*
     *  Modal Window Views
     */
    var ModalSlotView = Backbone.Marionette.ItemView.extend({
        events: {
            "click button.release-slot": "releaseSlot"
        },
        template: Handlebars.templates.slot_modal_template,
        /*
         *  Releasing a slot,
         */
        releaseSlot: function(event) {
            event.preventDefault();
            this.model.save({is_cancelled: true}, {
                success: _.bind(this.releaseSlotSuccess, this)
            });
        },
        releaseSlotSuccess: function(model, response, options) {
            model.collection.remove(model);
        }
    });

    var ModalShiftView = Backbone.Marionette.CompositeView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "sync", this.render);
        },
        events: {
            "click button.claim-slot": "claimSlot"
        },
        childView: ModalSlotView,
        childViewContainer: ".claimed-slots",
        template: Handlebars.templates.shift_modal_template,
        /*
         *  Claiming a shift slot
         */
        claimSlot: function(event) {
            event.preventDefault();
            this.model.claimSlot();
        }
    });

    var ModalRoleView = NestedCollectionCompositeView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "sync", this.render);
            if ( !this.model.isHydrated() ) {
                this.model.fetch();
            }
            this.collection.each(function(shift) {
                if ( !shift.isHydrated() ) {
                    shift.fetch();
                }
            });
        },
        childView: ModalShiftView,
        childViewContainer: ".shifts",
        childCollectionProperty: "claimed_slots",
        template: Handlebars.templates.role_modal_template
    });

    var ModalCellView = NestedCollectionCompositeView.extend({
        attributes: {
            class: "modal fade"
        },
        childView: ModalRoleView,
        childViewContainer: ".roles",
        childCollectionProperty: "shifts",
        template: Handlebars.templates.cell_modal_template
    });

    app.GridView = GridView;
    app.ModalCellView = ModalCellView;
});
