var app = app || {};

$(function(){
    "use-strict";

    var NestedCollectionCompositeView = Backbone.Marionette.CompositeView.extend({
        /*
         *  This view class instantiates a childview that is also a composite
         *  view, using a property of the child model as the collection value
         *  for the child view.
         */
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
    /*
     *  Pagination views
     */
    var GridPaginationView = Backbone.Marionette.ItemView.extend({
        initialize: function(options) {
            this.listenTo(this.model, "change", this.render);
        },
        tagName: "div",
        attributes: {
            class: "text-center"
        },
        template: Handlebars.templates.grid_pagination_template,
        events: {
            "click ul.pages li": "selectPage",
            "click a.previous-page": "decrementPage",
            "click a.next-page": "incrementPage",
        },
        selectPage: function(event) {
            event.preventDefault();
            var selectedPage = event.currentTarget.dataset.index;
            this.model.selectPage(selectedPage);
        },
        decrementPage: function(event) {
            event.preventDefault();
            this.model.selectPage(this.model.activePage() - 1);
        },
        incrementPage: function(event) {
            event.preventDefault();
            this.model.selectPage(this.model.activePage() + 1);
        }
    });

    /*
     *  shift grid table views
     */
    var GridCellView = Backbone.Marionette.ItemView.extend({
        /*
         *  View for a single cell in the shift grid.
         */
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
        /*
         *  View for a single row in the shift grid.
         */
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
        /*
         *  View for the full table of the shift grid.
         */
        initialize: function(options) {
            this.selectedDate = this.collection.first().get("date");
        },
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
        template: Handlebars.templates.shift_grid_template,
        filter: function(child, index, collection) {
            return child.get("date") === this.selectedDate;
        },
        changeDate: function(model, value, options) {
            this.selectedDate = value;
            this.render();
        }
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

    app.GridPaginationView = GridPaginationView;
    app.GridView = GridView;
    app.ModalCellView = ModalCellView;
});
