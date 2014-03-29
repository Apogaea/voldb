$(document).ready( function () {
    "use strict";

    /*
     *  Handle CSRF Token for ajax requests.
     *  Source: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
     */
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie("csrftoken");

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = "//" + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === origin + "/") ||
            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + "/") ||
            // or any other URL that isn"t scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /*
     *  Parallax Scrolling
     */    



    function isTouchDevice() {
       var el = document.createElement('div');
       el.setAttribute('ongesturestart', 'return;'); // or try "ontouchstart"
       return typeof el.ongesturestart === "function";
    }

    function parallaxScroll(){
        var scrolled = $(window).scrollTop();      
        $("body").css("background-position", "center "+((scrolled*0.25))+"px");
    }

    if (!isTouchDevice()) { 
        parallaxScroll();
        $(window).scroll(function(){
            parallaxScroll();
        });
    }    

    /*
     *  Shift grid view claiming and releasing.
     */
    function bindToClaimShift() {
        $("a.locked").click(function(e) {
            e.preventDefault();
        });
        $("a.shift-toggle:not('locked')").click(function(e) {
            e.preventDefault();
            // Render the modal window
            var template = Handlebars.compile($("#claim-modal").html());
            // The owner id to submit.
            var ownerId = _.isNull($(this).data("owner")) ? window.user : null;
            // Whether a verification code is required.
            var requiresCode = ($(this).data("restricted") && !_.isNull(ownerId));
            // The shift id.
            var shiftId = $(this).data("shift");
            // The depeartment id.
            var department = $(this).data("department");
            // The time that the shift starts
            var start = $(this).data("start");
            // The duration of the shift
            var shift_length = $(this).data("shift-length");
            var modal = $(template({
                restricted: requiresCode,
                owner: ownerId,
                shift: shiftId,
                department: department,
                start: start,
                shift_length: shift_length,
            }));
            modal.submit( function(e) {
                e.preventDefault();
                doShiftAPIRequest($(this));
            });
            modal.find("button.cancel").click( function() {
                $.modal.close();
            });
            modal.modal();
        });
    }
    function disableLockedShifts() {

    }

    function doShiftAPIRequest(form, link) {
        $.ajax(
        {
            url : form.attr("action"),
            type: "PUT",
            data : form.serializeArray(),
            success: function(data) {
                updateShiftCell(data);
                $.modal.close();
            },
            error: function(jqXHR)
            {
                var errors = form.find("ul.errors");
                errors.text("");
                if ( !_.isUndefined(jqXHR.responseJSON) ) {
                    _.each(_.pairs(jqXHR.responseJSON), function(error) {
                        var message = error[1];
                        errors.append($("<li>" + message + "</li>"));
                    });
                    $.ajax({
                        url : form.attr("action"),
                        type: "GET",
                        success: updateShiftCell
                    });
                } else {
                    errors.append($("<li>Something went terribly wrong... Try refreshing the page.</li>"));
                }
            }
        });
    }

    function updateShiftCell(data) {
        console.log("Updated shift")
        var link = $("a.shift-" + data.id);
        link.data("shift", data.id);
        link.data("restricted", data.requires_code);
        link.data("owner", data.owner);
        link.data("department", data.department);
        link.data("start", data.start);
        link.data("shift_length", data.shift_length);
        link.text(data.display_text);
        link.removeClass();
        link.addClass("shift-" + data.id);
        link.addClass("shift-toggle");
        if (data.owner) {
            link.addClass("claimed-shift");
        } else {
            link.addClass("open-shift");
            link.text("o p e n");
        }
    }

    function bindToggleDept() {
        $("th.department").click(function(e) {
            $(this).parent().find(".hideable").toggleClass("hidden");
        });
    }
    bindToggleDept()
  

    bindToClaimShift();
});
