$(document).ready(function(){
    var $swiperContainer = toggleSwiper();
    var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        spaceBetween: 30,
    });
    $swiperContainer.find('.swiper-wrapper').observe('childlist', function(){
        swiper.update();
        toggleSwiper(swiper);
    });

    //for the delete message box
    //trying to use jquery for event handling
    //got snipet from: http://www.sitepoint.com/10-jquery-ipad-code-snippets-plugins/
    var ua = navigator.userAgent,
    event = (ua.match(/iPad/i)) ? "touchstart" : "click";

    //opens the bigger image sliding div.. could be used for the receipt
    $(".receipt-taken").bind(event, function(){
        //if tooltip for item value was open then hide it 
        $('#tooltip-value').not('.hidden').toggleClass('hidden');
        //if tooltip for receipt was open then hide it
        $('#tooltip-receipt').not('.hidden').toggleClass('hidden');
        //slide the div open
        eleToggle('#image-detail','image-zoom-open','image-zoom-close'); 
        //check if we are reopening so we don't hide to avoid showing an empty div
        if ( $('#detail-receipt-content').hasClass('hidden') ){
            //show the receipt
            $('#detail-receipt-content').toggleClass('hidden');
        }

        //gray out background so user doesn't click on something else
        //while help message is open
        $('#overlay-no-spiner').toggleClass('hidden');
    });

    //closes the bigger image sliding div.. could be used for the receipt
    $("#close-image-detail").bind(event, function(){
        //hide the gray overlay
        $('#overlay-no-spiner').not('.hidden').toggleClass('hidden');
        eleToggle('#image-detail','image-zoom-open','image-zoom-close'); 
    });

    //help text for item value
    $('#item-value').bind(event, function(){
        //if receipt was open then hide it 
        $('#detail-receipt-content').not('.hidden').toggleClass('hidden');
        //if tooltip for receipt was open then hide it
        $('#tooltip-receipt').not('.hidden').toggleClass('hidden');
        //slide the div open
        eleToggle('#image-detail','image-zoom-open','image-zoom-close');
        //check if we are reopening so we don't hide to avoid showing an empty div
        if ( $('#tooltip-value').hasClass('hidden') ){
            $('#tooltip-value').toggleClass('hidden');
        }
        //gray out background so user doesn't click on something else
        //while help message is open
        $('#overlay-no-spiner').toggleClass('hidden');
    });

    $('.tooltip-item-receipt').bind(event, function(){
        //if receipt was open then hide it 
        $('#detail-receipt-content').not('.hidden').toggleClass('hidden')
        //if tooltip for item value was open then hide it 
        $('#tooltip-value').not('.hidden').toggleClass('hidden');
        //slide the div open
        eleToggle('#image-detail','image-zoom-open','image-zoom-close');
        //check if we are reopening so we don't hide to avoid showing an empty div
        if ( $('#tooltip-receipt').hasClass('hidden') ){
            $('#tooltip-receipt').toggleClass('hidden');
        }
        //gray out background so user doesn't click on something else
        //while help message is open
        $('#overlay-no-spiner').toggleClass('hidden');
    });

    $(".images-delete a").bind(event, function() {
        var $ele = $(this).parent().siblings('div.delete-image');
        eleToggle($ele, 'delete-open', 'delete-close');
    });

    $("a.btn-no").bind(event, function() {
        var $ele = $(this).parent();
        eleToggle($ele, 'delete-open', 'delete-close');
    });

    $("a.btn-yes").bind(event, function() {
        var $ele = $(this).parent();
        eleToggle($ele, 'delete-open', 'delete-close');
        var $activeSlide = $('.swiper-slide-active');
        $('input[value="' + $activeSlide.find('img').attr('src') + '"]').remove();
        $activeSlide.remove();
        swiper.update();
    });

    function toggleSwiper(swiper) {
        var $swiperContainer = $('.swiper-container');
        var slideCount = $swiperContainer.find('.swiper-slide').length;
        var hasImages = slideCount > 0;
        $swiperContainer.toggle(hasImages);
        $('.no-jewelry-pics').toggle(!hasImages);
        //hide pagination and delete image button when slider is empty
        $('.swiper-pagination').toggleClass('hidden', !hasImages);
        $('.images-delete').toggleClass('hidden', !hasImages);
        $('.jewelry-photo-button button').toggleClass('jewelry-photo-button-active', hasImages);
        if (hasImages) {
            if (typeof swiper != 'undefined') {
                swiper.slideTo(slideCount - 1);
            }
        } else {
            $input = $('.jewelry-photo-input input');
            $input.wrap('<form>').parent('form').trigger('reset');
            $input.unwrap();
        }
        return $swiperContainer;
    }
});
