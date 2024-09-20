// Page functions
function scalePage() {
    //adjust the font sizes
    let total_width = $(window).outerWidth();
    let base_em = 3;
    let base_width = 1280.0;
    let scale = base_em/base_width;
    let golden_ratio = (1.0+Math.sqrt(5))/2.0;

    let col1 = total_width * scale;
    let col2 = total_width * scale * (1.0/golden_ratio);
    let col3a = total_width * scale * (1.0/golden_ratio) * (1.0/golden_ratio);
    let col3b = total_width * scale * (1.0/golden_ratio) * (1.0/golden_ratio) * (1.0/golden_ratio);

    $("#column1 h1").css({"font-size":0.95 * col1 + "em"});
    $("#column2 li").css({"font-size":0.9 * col2 + "em"});
    $("#column3 h2").css({"font-size":1.262 * col3a + "em"});
    $("#column3 h3").css({"font-size":1.1 * col3a + "em"});
    $("#column3 h4").css({"font-size":col3a + "em"});
    $("#column3 h5").css({"font-size":col3a + "em"});
    $("#column3 p, #column3 li").css({"font-size":col3a + "em"});
    $("#column1 #links p").css({"font-size":col3a + "em"});

    //adjust the vertical margins and padding to line up all three columns
    let total_height = $(window).outerHeight();

    $("#column1, #column2, #column3").css({"height":total_height + "px"});

    let col1_line_height_split = $("#column1 h1").css("line-height").split("px");

    let col1_line_height;
    let col1_line_height_in_pix;
    if (col1_line_height_split.length > 1) {
        // the line height is already in pixels
        col1_line_height = parseFloat(col1_line_height_split[0]);
        col1_line_height_in_pix = true;
    } else {
        // the line height is a percentage of the font size
        col1_line_height = col1_line_height_split[0];
        col1_line_height_in_pix = false;
    }

    let col1_font_size = parseFloat($("#column1 h1").css("font-size").split("px")[0]);

    let links_height = $("#column1 #links").outerHeight(true);
    if (links_height === 0)
        links_height = $("#column1 #links p").outerHeight(true);
    let col1_h1_height = $("#column1 h1").height();

    let col1_baseline;
    if (col1_line_height_in_pix)
      col1_baseline = col1_line_height - col1_font_size;
    else
      col1_baseline = (col1_line_height - 1) * col1_font_size;

    let col2_li_bottom_margin = col1_baseline * 1.3;

    $("#column2 li").css({"margin-bottom":col2_li_bottom_margin + "px"});

    let top_position = total_height * (1.0 - 1.0 / golden_ratio) - col1_baseline;

    let top_adjust;
    if ( $("#column2 ul").outerHeight(true) + top_position + col1_baseline > total_height ) {
        top_adjust = top_position - ($("#column2 ul").outerHeight(true) + top_position + col1_baseline - total_height);
        if (top_adjust < 0)
            top_adjust = 0;
    } else {
        top_adjust =  top_position;
    }

    $("#column1 h1").css({"top":top_adjust + "px", "position":"relative"});
    $("#column1 #links").css({"top":(top_adjust + col1_h1_height) + "px", "position":"absolute"});
    $("#column2 ul").css({"top":(top_adjust + col1_baseline) + "px", "position":"relative"});
    $("#column3 .section").css({"top":(top_adjust + col1_baseline) + "px", "position":"absolute"});
}

function showPage() {
    let dur = 500.0;
    let overlap = 0.75;
    $("#column1,#column2,#column3").removeClass("invisible");
    $("#column1,#column2,#column3").css({"opacity":0});
    $("#column1").fadeIn({duration:dur, progress:function(a, b, c) {
        if ( c < dur * overlap ) {
            $("#column2").fadeIn({duration:dur, progress:function(a, b, c) {
                if ( c < dur * overlap ) {
                    $("#column3").fadeIn(dur);
                }
            }});
        }
    }});
}

function showContent(content_id) {
    let dur = 500.0;
    let overlap = 0.5;
    let curr_content = $("#column3 .section.active");
    // scalePage();

    $("#column3").animate(
      {scrollTop: 0},
        {duration: dur * overlap}
    );
    curr_content.fadeOut(
        {   duration: dur,
            progress: function(a, b, c) {
                if ( c < dur * overlap ) {
                    $("#column3").scrollTop(0);
                    // curr_content.addClass("unflow")
                    // $("#"+content_id).show();
                    $("#"+content_id).fadeIn(
                        {   duration:dur,
                            complete: function() {
                                $("#"+content_id).addClass("active");
                            }
                        }
                    );
                }
            },
            complete: function() {
                curr_content.removeClass("active");
                curr_content.hide();
            }
        }
    );
}

// Code to run when the page is ready
$(document).ready(function(){
  const root = document.querySelector(':root');
  const total_width = $(window).outerWidth(),
        max_width = parseInt(getComputedStyle(root).getPropertyValue('--max-width'));
    $("#column2").append("<ul></ul>");
    $("#column3 .section").each(function(index){
        $("#column2 ul").append("<li>"+jQuery.trim($(this).children("h1").text())+"</li>");
        if ( $(this).attr("id") === "summary" ) {
            $(this).addClass("active");
        } else {
            if ( total_width >= max_width) {
                $(this).hide();
            }
        }
    });
    // Load any external scripts that are needed.
    (function() {
        $.getScript("js/classes.js", function() {
            let page_nav = new CVNav("#column2");
        });
    }());
    $("#links p").mouseenter(function(event) {
        $(event.delegateTarget).css("cursor","pointer");
        $(event.delegateTarget).addClass("hovered");
    });
    $("#links p").mouseleave(function(event) {
        $(event.delegateTarget).css("cursor","auto");
        $(event.delegateTarget).removeClass("hovered");
    });

    let col1 = document.getElementById('column1'),
        col2 = document.getElementById('column2'),
        col3 = document.getElementById('column3');

    col1.classList.toggle('fadeIn');
    col2.classList.toggle('fadeIn');
    col3.classList.toggle('fadeIn');


    // scalePage();
    // showPage();

});

// Code to run when the window is resized
$(window).resize(function(){
    const root = document.querySelector(':root');
    const total_width = $(window).outerWidth(),
          max_width = parseInt(getComputedStyle(root).getPropertyValue('--max-width'));
    $("#column3 .section").each(function(index){
        $(this).show();
        if ( !$(this).hasClass("active") ) {
            if ( total_width >= max_width) {
                $(this).hide();
            }
        }
    });
});
