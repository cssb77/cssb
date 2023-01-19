# 从flask中导入request对象
from flask import Flask, render_template, request
from data import star_data

app = Flask(__name__)


# 路由：返回“生日表单页面”
@app.route('/date')
def birthday():
    return render_template('date.html')


# 路由：返回“星座详情页面”
# 【提示2】设置服务器接收post请求
@app.route('/star',methods=["POST"])
def star():
    month = int(request.form['month'])
    day = int(request.form['day'])
    dates = [20, 19, 21, 21, 21, 22, 23, 23, 23, 24, 23, 22]
    stars = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
    if day < dates[month-1]:
        return render_template('star.html', t_star_data=star_data.star_data[month-1])
    else:
        # 摩羯座是第1位
        return render_template('star.html', t_star_data=star_data.star_data[0 if month == 12 else month])


if __name__ == '__main__':
    app.run(port=5001, debug=True)


