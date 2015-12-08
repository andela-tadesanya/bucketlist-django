/* get text from all divs of class messages */
$('.messages').each(function () {
    toast_text = $(this).text();
    if (toast_text != ""){
        Materialize.toast(toast_text, 10000);
    }
});

