window.onload = function() {
    data = document.getElementById('data').innerHTML
    name = document.getElementById('name').innerHTML
    originData = data.slice(1,data.length-1)
    objData = originData.split(',')

    // 配置options
    echarts.init(document.getElementById('chart')).setOption({
        title: {
        text: name,
        left: 'center'
    },
    // 图表的位置
    grid: {
        position: 'center',
     },
     tooltip : {
     //雷达图的tooltip不会超出div，也可以设置position属性，position定位的tooltip 不会随着鼠标移动而位置变化，不友好
        confine: true,
        enterable: true, //鼠标是否可以移动到tooltip区域内
     },
    radar: {
        splitNumber: 5, // 雷达图圈数设置
        indicator: [
        {
            name: '防御分值', max: 5,
            //若将此属性放在radar下，则每条indicator都会显示圈上的数值，放在这儿，只在通信这条indicator上显示
            axisLabel: {
                show: true,
                fontSize: 12,
                color: '#838D9E',
                showMaxLabel: false, //不显示最大值，即外圈不显示数字30
                showMinLabel: true, //显示最小数字，即中心点显示0
            },
        },
        { name: '攻击分值', max: 5},
        { name: '爱心分值', max: 5},
        { name: '装扮分值', max: 5},
        { name: '智慧分值', max: 5}
        ]
    },
    series: [{
        name: name, // tooltip中的标题
        type: 'radar', //表示是雷达图
        symbol: 'circle', // 拐点的样式，还可以取值'rect','angle'等
        symbolSize: 8, // 拐点的大小

        areaStyle: {
            normal: {
                width: 1,
                opacity: 0.2,
            }
        },
        data: [
            {
                value: objData,
                name: name + '英雄维度分值',

                //在拐点处显示数值
                label: {
                    normal: {
                        show: true
                    }
                }
            }
        ]
    }]
    })
}