$(document).ready(function() {
    $('.jewelry-photo-input input[type="file"]').on('change', function(e) {
        e.preventDefault();
        $('.jewelry-pic').hide();
        $('.jewelry-photo-button .fa-check-square').hide();
        if (this.files.length === 0) {
            $('.jewelry-photo-button .fa-photo').show();
            $('#id_jewelry_image_url').val('');
            return;
        }
        
        $('.overlay-screen').toggleClass('hidden');
        
        var imageFile = this.files[0];
        var fileName = window.globals.transactionId + '-' + imageFile.name;
        $.get(window.globals.signedS3RequestUrl + '?file_name=' + fileName + '&file_type=' + imageFile.type, function(response){
            $.ajax({
                url: response.signed_request,
                method: 'PUT',
                contentType: imageFile.type,
                headers: {
                    'x-amz-acl': 'public-read'
                },
                processData: false,
                dataType: "jsonp",
                data: imageFile,
                success: function(){
                    $('.overlay-screen').toggleClass('hidden');

                    $('.jewelry-photo-button button').addClass('jewelry-photo-button-active');

                    $('.jewelry-photo-input').closest('form').append(
                        '<input type="hidden" id="id_jewelry_image_urls" name="jewelry_image_urls" value="' + response.url + '"/>'
                    );
                    $('.swiper-wrapper').append(
                        '<div class="swiper-slide"><img src="' + response.url + '"/>'
                    );
                }
            });
        });
    });
});
