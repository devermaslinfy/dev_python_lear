$(document).ready(function(){
    var username = Cookies.get('username');
    var $rememberme = $('#rememberme');
    var $username = $('#username');
    if (username) {
        $username.val(username);
        $rememberme.prop('checked', true);
    }
    $rememberme.change(function(){
        if ($(this).prop('checked')) {
            Cookies.set('username', $('#username').val());
        } else {
            Cookies.remove('username');
        }
    });
});
