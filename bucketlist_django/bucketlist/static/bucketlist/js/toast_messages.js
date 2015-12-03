/* get text from all divs of class messages */
toast_text = $('.messages').text();

if (toast_text != ""){
Materialize.toast(toast_text, 10000);
}