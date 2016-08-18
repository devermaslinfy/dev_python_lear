$(document).ready(function() {
    $('.receipt-photo-input input[type="file"]').on('change', function(e) {
        e.preventDefault();
        $('.receipt-photo-button .fa-check-square').hide();
        if (this.files.length === 0) {
            $('.receipt-photo-button .fa-photo').show();
            $('#id_receipt_image_url').val('');
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
                data: imageFile,
                success: function(){
                    $('.overlay-screen').toggleClass('hidden');
                    $('.receipt-photo-input').toggleClass('hidden');
                    $('#receipt-photo-taken').toggleClass('hidden');
                    $('#id_receipt_image_url').val(response.url);
                    $('#receipt-image').html('<img src="' + response.url + '"/>');
                }
            });
        });
    });
});
