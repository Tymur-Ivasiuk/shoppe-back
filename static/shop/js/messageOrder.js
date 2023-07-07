var yesMsg = document.getElementById('yes-msg');

$(document).ready(function() {
    setTimeout(disabledMsg, 5000);
});

function disabledMsg() {
    yesMsg.classList.remove('active-msg');
}