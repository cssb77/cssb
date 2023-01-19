# 从flask中导入request对象
from flask import Flask, render_template, request
from data import star_data

app = Flask(__name__)


# 路由：返回“昵称表单页面”
@app.route('/index')
def index():
    return render_template('index.html')


# 路由：返回“壮猿图片页面”
# 【提示2】设置服务器接收post请求
@app.route('/hello', methods=['GET'])
def hello():
    # 【提示3】获取数据名称nickname的值，并保存在变量nickname中
    request.args[""]
    # 【提示3】为模板变量t_nickname赋值
    return render_template('hello.html')


# 路由：返回“生日表单页面”
@app.route('/date')
def birthday():
    return render_template('date.html')


# 路由：返回“星座详情页面”
# 【提示5】设置服务器接收get请求
@app.route('/star'methods=["GET"])
def star():
    # 出生日期-月
    month = int(request.args['month'].strip(' '))
    # 出生日期-日
    day = int(request.args['day'].strip(' '))
    # 星座之间的转折日
    dates = [20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22]
    # 星座列表集合
    stars = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
    if day < dates[month-1]:
        return render_template('star.html', t_star_data=star_data.star_data[month-1])
    else:
        # 摩羯座是第1位
        return render_template('star.html', t_star_data=star_data.star_data[0 if month == 12 else month])


if __name__ == '__main__':
    app.run(port=5001, debug=True)


