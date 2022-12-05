var buttonAdd = document.getElementById('add');
var yesMsg = document.getElementById('yes-msg');


buttonAdd.onclick = function() {
    yesMsg.classList.add('active-msg');
    setTimeout(disabledMsg, 7000);
}
function disabledMsg() {
    yesMsg.classList.remove('active-msg');
}