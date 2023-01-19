var myfile = document.querySelector('#chooseimg');
var fxfile = document.querySelector('.fxfile');
var uploadbtn = document.querySelector('.uploadbtn');
myfile.onchange = function(){
  if(this.files){
      fxfile.style.opacity = 1;
      uploadbtn.style.visibility = 'visible';
  }
}