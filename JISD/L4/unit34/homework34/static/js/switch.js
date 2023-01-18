window.onload = function(){
    button = document.getElementById('switchOp')
    elements = document.getElementsByName('op')
    op = elements[0]
    //查找显示‘汉语’和‘英语’的两个input标签
    elements = document.querySelectorAll('.inputFan')
    label1 = elements[0]
    label2 = elements[1]

    console.log(label1)

    //重置显示的内容
    if(op.value == '英译汉'){
        label1.setAttribute('placeholder','英语')
        label2.setAttribute('placeholder','汉语')
    }else if (op.value == '汉译英'){
        //修改value和修改placeholder的区别在于value显示出来是黑色的，placeholder显示出来是灰色的
        //label1.value = '汉语'
        //label2.value = '英语'
        label1.setAttribute('placeholder','汉语')
        label2.setAttribute('placeholder','英语')
    }

    //为按钮绑定点击事件
    button.onclick = function(){
        currentValue = op.value;
        console.log('点击事件' + currentValue)
        /*切换方式其实可以写成开关形式，会更好。by-wsk*/
        if (currentValue == '英译汉'){
            label1.setAttribute('placeholder','汉语')
            label2.setAttribute('placeholder','英语')
            op.value = '汉译英'
        }else if (currentValue == '汉译英'){
            label1.setAttribute('placeholder','英语')
            label2.setAttribute('placeholder','汉语')
            op.value = '英译汉'
        }
    }
}
