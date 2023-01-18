var btns = document.getElementsByTagName("button")
var yuan = document.getElementById("yuan")

if(btns[0]){
	btns[0].onclick = function() {
		yuan.src = "img/niu.gif"
	}
}
if(btns[1]){
	btns[1].onclick = function() {
		yuan.src = "img/pai.gif"
	}
}
if(btns[2]){
	btns[2].onclick = function() {
		yuan.src = "img/huixuan.gif"
	}
}
if(btns[3]){
	btns[3].onclick = function() {
		yuan.src = "img/stand.png"
	}
}