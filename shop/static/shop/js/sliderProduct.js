$(document).ready(function() {
  if ($('.product-image-small-wrap').length > 4) {
    $('.slider-main').slick({
      slidesToShow: 1,
      arrows: false,
      dots: true,
      asNavFor: '.slider-nav',
      // vertical: true,
      speed: 500,
      fade: true,
      cssEase: 'linear',

    });

    $('.slider-nav').slick({
      slidesToShow: 4,
      asNavFor: '.slider-main',
      vertical: true,
      focusOnSelect: true,
      arrows: false,
      autoplay: false,

    });
  } else {
    $('.slider-main').slick({
      slidesToShow: 1,
      arrows: false,
      dots: true,
      // vertical: true,
      speed: 500,
      fade: true,
      cssEase: 'linear',

    });

    $('.slider-nav').slick({
      slidesToShow: 4,
      asNavFor: '.slider-main',
      vertical: true,
      focusOnSelect: true,
      arrows: false,
      autoplay: false,

    });
  }
     
});