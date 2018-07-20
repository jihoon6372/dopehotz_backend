


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