$(function () {
    var lastScrollTop = 0,
        delta = 15;
    $(window).scroll(function (event) {
        var st = $(this).scrollTop();
        if (Math.abs(lastScrollTop - st) <= delta)
            return;
        if ((st > lastScrollTop) && (lastScrollTop > 0)) {
            $("#header_m").css("top", "-40px");
            $(".menu_btn_m").css("top", "-40px");
        } else {
            $("#header_m").css("top", "0px");
            $(".menu_btn_m").css("top", "0px");
        }
        lastScrollTop = st;
    });
});

$(function () {
    $(window).scroll(function () {
        var winTop = $(window).scrollTop();
        if (winTop >= 30) {
            $("#header_m").css("background-color", "#1a1a1a");
        } else {
            $("#header_m").css("background-color", "#242425");
        }
    });
});


// $(".menu_btn_m").click(function () {
//     if ($(".menu_btn_m").hasClass('open')){
//         $(".menu_btn_m,.layout_menu,body").removeClass("open");
//         $(".page_cover").fadeOut(200);
//     }else {
//         $(".menu_btn_m,.layout_menu,body").addClass("open");
//         $(".page_cover").fadeIn(200);
//     }
// });

window.onhashchange = function () {
    if (location.hash != "#menu-open") {
        $(".menu_btn_m,.layout_menu,body").removeClass("open");
        $(".page_cover").fadeOut(200);
    }
};