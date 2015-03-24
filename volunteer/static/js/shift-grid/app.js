var app = app || {};

$(function(){
    "use-strict";

    var ShiftGridApplication = Backbone.Marionette.Application.extend({
        initialize: function(options) {
            this.shiftData = new app.GridRows(options.rows);
            this.shiftLayout = this.initializeLayout(options.el);
            // Shift Grid
            var gridView = new app.GridView({
                collection: this.shiftData
            });
            this.shiftLayout.grid.show(gridView);
            this.listenTo(gridView, "cell:click", this.initializeModal);

            // Pagination
            var paginationView = new app.GridPaginationView({
                model: new app.GridPageInfo(this.shiftData.getPageInfo()),
                collection: this.shiftData
            });
            this.shiftLayout.pagination.show(paginationView);
        },
        initializeModal: function(cellView) {
            /*
             *  The cell click event is bubbled all the way up to here, where
             *  we show the modal window where they can claim the shift.
             */
            var cellModal = new app.ModalCellView({
                model: cellView.model,
                collection: cellView.model.get("roles"),
            });
            this.shiftLayout.cell_modal.show(cellModal);
            cellModal.$el.modal("show");
        },
        initializeLayout: function(el) {
            return new app.ShiftGridLayout({
                application: this,
                el: el
            });
        },
    });

    app.ShiftGridApplication = ShiftGridApplication;
});
