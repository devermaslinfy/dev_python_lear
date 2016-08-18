function eleToggle(ele, openCSS, closeCSS){

  if ( $(ele).hasClass(closeCSS) ){
    $(ele).toggleClass(openCSS);
  } else if ( $(ele).hasClass(openCSS) ){
    $(ele).toggleClass(closeCSS);
  }
  
}


//for the delete message box
    //trying to use jquery for event handling
    //got snipet from: http://www.sitepoint.com/10-jquery-ipad-code-snippets-plugins/
    var ua = navigator.userAgent,
    event = (ua.match(/iPad/i)) ? "touchstart" : "click";

    //opens the bigger image sliding div.. could be used for the receipt
    $(".open-slider, .close-slider").bind(event, function(){
        //slide the div open
        eleToggle('#image-detail','image-zoom-open','image-zoom-close'); 
        //gray out background so user doesn't click on something else
        //while help message is open
        //$('#overlay-no-spiner').toggleClass('hidden');
    });
