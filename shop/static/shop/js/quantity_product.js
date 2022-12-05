var numCount = document.getElementById('num_count');
var plusBtn = document.getElementById('button_plus');
var minusBtn = document.getElementById('button_minus');

if (numCount.max > 1){
  plusBtn.onclick = function() {
    var qty = parseInt(numCount.value);
    if (parseInt(numCount.value) < numCount.max){
      qty = qty + 1;
    }
    numCount.value = qty;

    if (parseInt(numCount.value) == numCount.max) {
      plusBtn.className = "disabled"
    }
    minusBtn.className = ""
  }

  minusBtn.onclick = function() {
    var qty = parseInt(numCount.value);
    if (parseInt(numCount.value) > numCount.min){
      qty = qty - 1;
    }
    numCount.value = qty;

    if (parseInt(numCount.value) == numCount.min) {
      minusBtn.className = "disabled"
    }
    plusBtn.className = ""
  }
}

