$(function() {
  function HeaderActiveEventSelector(el) {
    $.extend(this, {
      el: el,
      onChange: function(event) {
        console.log("changed");
        debugger;
      }
    })

    $(this.el).on("change", $.proxy(this.onChange, this));
  }

  window.HeaderActiveEventSelector = HeaderActiveEventSelector;
});
