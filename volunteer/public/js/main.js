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

    function bindToClaimShiftForms() {
        $("form.claim-shift").submit(function(e) {
            e.preventDefault();
            var _this = this;
            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            var ownerInput = $(this).children("input[name='owner']");
            var submitInput = $(this).children("input[type='submit']");
            var tableCell = $(this).parent('td');
            $.ajax(
            {
                url : formURL,
                type: "PUT",
                data : postData,
                success: function(data, textStatus, jqXHR)
                {
                    if ( _.isNull(data.owner) ){
                        ownerInput.attr("value", window.user);
                    } else {
                        ownerInput.attr("value", "");
                    }

                    submitInput.attr("value", data.display_text);
                    tableCell.toggleClass("claimed");
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    //if fails what should we do?
                }
            });
        });
    }

    parallaxScroll();
    bindToClaimShiftForms();
});
