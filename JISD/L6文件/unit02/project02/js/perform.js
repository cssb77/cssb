var btns = document.getElementsByTagName("button")
var yuan = document.getElementById("yuan")
if(btns[0]){
	btns[0].onclick = function() {
		yuan.src = "img/jump.gif"
	}
}
if(btns[1]){
	btns[1].onclick = function() {
		yuan.src = "img/stand.png"
	}
}
