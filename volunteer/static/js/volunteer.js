$(function() {
  function HeaderActiveEventSelector(el) {
    $.extend(this, {
      el: el,
      onChange: function(event) {
        console.log("changed");
        var select = event.currentTarget;
        $.ajax({
          url: select.form.action,
          method: select.form.method,
          data: JSON.stringify({active_event: select.value}),
          dataType: "json",
          contentType: "application/json",
          error: function(jqXHR, textStatus, errorThrown) {
            console.error(errorThrown);
          }
        })
      }
    })

    $(this.el).on("change", $.proxy(this.onChange, this));
  }

  window.HeaderActiveEventSelector = HeaderActiveEventSelector;
});
