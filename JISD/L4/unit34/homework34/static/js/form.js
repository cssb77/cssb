function checkNum() {
    var total = 0;
    inputList = document.querySelectorAll('.calculate')
    for(var i = 0;i < inputList.length;i++) {
        total += parseInt(inputList[i].value)
    }
    if(total > 20) {
        event.preventDefault()
        alert('各项总技能值不能超过20哦！')
    }
}