


// var slideHeight = $(document).height();
// var slideWidth = $(document).width();

// $('.main_carousel').css('height', slideHeight - 20);
// $('.main_carousel').css('width', slideWidth);
var main_carousel = $('.main_carousel');
main_carousel.owlCarousel({
    items: 1,
    center: true,
    loop: true,
    nav: false,
    mouseDrag : false
});
main_carousel.on('mousewheel', '.owl-stage', function (e) {
    if (e.deltaY > 0) {
        main_carousel.trigger('prev.owl');
    } else {
        main_carousel.trigger('next.owl');
    }
    e.preventDefault();
});

var track_select = $(".post_carousel");

track_select.owlCarousel({
    margin:50,
    loop:false,
    autoWidth:true,
    items:1,
    center:true,
	autoplay:false,
    URLhashListener:false,
    nav: true,
});

$(".prev_select").click(function () {
    track_select.trigger('prev.owl.carousel');
});

$(".next_select").click(function () {
    track_select.trigger('next.owl.carousel');
});