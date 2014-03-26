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
    $(window).scroll(function(){
        parallaxScroll();
    });

    function parallaxScroll(){
        var scrolled = $(window).scrollTop();
        //$("#parallax-bg1").css("top",(0-(scrolled*.25))+"px");
        //$(window).css("background-position-y", (0-(scrolled*1.25))+"px");            
        $("body").css("background-position", "center "+(0-(scrolled*0.45))+"px");
    }

    /*
     *  Shift grid view claiming and releasing.
     */
    function bindToClaimShift() {
        $("a.shift-toggle").click(function(e) {
            e.preventDefault();
            var link = this;
            // Render the modal window
            var template = Handlebars.compile($("#claim-modal").html());
            // The owner id to submit.
            var ownerId = _.isNull($(this).data("owner")) ? window.user : null;
            // Whether a verification code is required.
            var requiresCode = ($(this).data("restricted") && !_.isNull(ownerId));
            // The shift id.
            var shiftId = $(this).data("shift");
            // The depeartment id.
            var departmentId = $(this).data("department");
            // The time that the shift starts
            var time = $(this).data("start_time");
            // The duration of the shift
            var shift_length = $(this).data("shift_length");
            var modal = $(template({
                restricted: requiresCode,
                owner: ownerId,
                shift: shiftId,
                department: departmentId,
                time: time,
                shift_length: shift_length,
            }));
            modal.submit( function(e) {
                e.preventDefault();
                doShiftAPIRequest($(this), $(link));
            });
            modal.find("button.cancel").click( function() {
                $.modal.close();
            });
            modal.modal();
        });
    }

    function doShiftAPIRequest(form, link) {
        $.ajax(
        {
            url : form.attr("action"),
            type: "PUT",
            data : form.serializeArray(),
            success: function(data, textStatus, jqXHR)
            {
                link.data("shift", data.id);
                link.data("restricted", data.requires_code);
                link.data("owner", data.owner);
                link.data("department", data.department);
                link.data("time", data.start_time);
                link.data("shift_length", data.shift_length);
                link.text(data.display_text);
                $.modal.close();
            },
            error: function(jqXHR, textStatus, errorThrown)
            {
                var errors = form.find("ul.errors");
                errors.text("");
                _.each(_.pairs(jqXHR.responseJSON), function(error) {
                    var message = error[1];
                    errors.append($("<li>" + message + "</li>"));
                });
            }
        });
    }

    parallaxScroll();
    bindToClaimShift();
});
