(function($) {
  
  "use strict";  

  $(window).on('load', function() {


  /* Page Loader active */
  $('#preloader').fadeOut();

  /* slider */
  var cosiness = document.getElementById('slider-value').innerHTML;
  var margin_need = 600*cosiness-30;
  if ($(window).width() < 620) {
    $('.slider').css({width: '300px'});
    $('#WholeBar').css({width: '300px'});
    margin_need = 300*cosiness-30;
  }
  $('.circle').css({marginLeft: margin_need});
  if(cosiness<=0.35){
    $('.circle').css({backgroundColor: '#4bc67c'});
    $('#index-message').append('<b>comfortable<b/>.');
  } else if (cosiness > 0.35 && cosiness<=0.70){
    $('.circle').css({backgroundColor: '#dac41d'});
    $('#index-message').append('<b>very comfortable</b>.');
  } else if (cosiness > 0.70 && cosiness<=0.85){
    $('.circle').css({backgroundColor: '#d4852b'});
    $('#index-message').append('<b>uncomfortable</b>.');
  } else {
    $('.circle').css({backgroundColor: '#b94a48'});
    $('#index-message').append('<b>very uncomfortable</b>.');
  }

  var humidex = document.getElementById('humidex-value').innerHTML;
  var margin_humidex = 300*humidex-25;
  $('#humidex-circle').css({marginLeft: margin_humidex});
  $('#humidex-bar').css({width: margin_humidex});
  if(humidex<=0.33){
    $('#humidex-message').append("<b>low<b/>");
  } else if (humidex>0.33 && humidex<=0.66){
    $('#humidex-message').append("<b>medium</b>");
  } else {
    $('#humidex-message').append("<b>high</b>");
  }

  var air= document.getElementById('air-value').innerHTML;
  var margin_air = 300*air-25;
  $('#air-circle').css({marginLeft: margin_air});
  $('#air-bar').css({width: margin_air});
  if(air<=0.33){
    $('#air-message').append("<b>good<b/>");
  } else if (air>0.33 && air<=0.66){
    $('#air-message').append("<b>acceptable</b>");
  } else {
    $('#air-message').append("<b>unacceptable</b>");
  }

  var environment = document.getElementById('environment-value').innerHTML;
  var margin_environment = 300*environment-25;
  $('#environment-circle').css({marginLeft: margin_environment});
  $('#environment-bar').css({width: margin_environment});
  if(environment<=0.33){
    $('#environment-message').append("<b>good<b/>");
  } else if (environment>0.33 && environment<=0.66){
    $('#environment-message').append("<b>acceptable</b>");
  } else {
    $('#environment-message').append("<b>alarming</b>");
  }

  // Sticky Nav
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 50) {
            $('.scrolling-navbar').addClass('top-nav-collapse');
        } else {
            $('.scrolling-navbar').removeClass('top-nav-collapse');
        }
    });

    // one page navigation 
    $('.navbar-nav').onePageNav({
      currentClass: 'active'
    });

    /* slicknav mobile menu active  */
    $('.mobile-menu').slicknav({
        prependTo: '.navbar-header',
        parentTag: 'liner',
        allowParentLinks: true,
        duplicate: true,
        label: '',
        closedSymbol: '<i class="lni-chevron-right"></i>',
        openedSymbol: '<i class="lni-chevron-down"></i>',
      });

      /* WOW Scroll Spy */
     var wow = new WOW({
      //disabled for mobile
        mobile: false
    });

    wow.init();

     /* Testimonials Carousel */
    var owl = $("#testimonials");
      owl.owlCarousel({
        loop: true,
        nav: false,
        dots: false,
        center: true,
        margin: 15,
        slideSpeed: 1000,
        stopOnHover: true,
        autoPlay: true,
        responsiveClass: true,
        responsiveRefreshRate: true,
        responsive : {
            0 : {
                items: 1
            },
            768 : {
                items: 1
            },
            960 : {
                items: 1
            },
            1200 : {
                items: 1
            },
            1920 : {
                items: 1
            }
        }
      });  

     /*  Slick Slider */
    $('.slider-center').slick({
      centerMode: true,
      centerPadding: '60px',
      slidesToShow: 3,
      responsive: [
        {
          breakpoint: 768,
          settings: {
            arrows: false,
            centerMode: true,
            centerPadding: '40px',
            slidesToShow: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            arrows: false,
            centerMode: true,
            centerPadding: '40px',
            slidesToShow: 1
          }
        }
      ]
    });
    

    /* Back Top Link active */
    var offset = 200;
    var duration = 500;
    $(window).scroll(function() {
      if ($(this).scrollTop() > offset) {
        $('.back-to-top').fadeIn(400);
      } else {
        $('.back-to-top').fadeOut(400);
      }
    });

    $('.back-to-top').on('click',function(event) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: 0
      }, 600);
      return false;
    });

    /* Map Form Toggle */
    $('.map-icon').on('click',function (e) {
        $('#conatiner-map').toggleClass('panel-show');
        e.preventDefault();
    });

  });      

}(jQuery));
