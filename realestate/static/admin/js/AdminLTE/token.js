$(document).ready(function () {

    function randomString(string_length) {
        var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
        string_length = string_length || 20;
        var randomstring = '';
        for (var i = 0; i < string_length; i++) {
            var rnum = Math.floor(Math.random() * chars.length);
            randomstring += chars.substring(rnum, rnum + 1);
        }
        return randomstring;
    }

    $(".generate-key").click(function(e){
        e.preventDefault();
        var key_field = $("#id_key");
        var hash = CryptoJS.SHA1(randomString());
        key_field.val(hash);
    });
});