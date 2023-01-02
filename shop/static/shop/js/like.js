var likeBtn = document.getElementById('button_like');
var likeIconOff = document.getElementById('like_icon-off');
var likeIconOn = document.getElementById('like_icon-on');

likeBtn.onclick = function() {
    likeBtn.classList.toggle('active');
}