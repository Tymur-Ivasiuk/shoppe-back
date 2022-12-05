var likeBtn = document.getElementById('button_like');
var likeIconOff = document.getElementById('like_icon-off');
var likeIconOn = document.getElementById('like_icon-on');

likeBtn.onclick = function() {
    if(likeIconOff.classList.contains('active')){
        likeIconOff.classList.remove('active');
        likeIconOn.classList.add('active');
    } else {
        likeIconOn.classList.remove('active');
        likeIconOff.classList.add('active');
    }
}