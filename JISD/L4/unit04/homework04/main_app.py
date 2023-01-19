# 从flask模块导入Flask
from flask import Flask,render_template
app = Flask(__name__)



# 【提示1】定义路由，资源地址为'/main'
@app.route('/main')
def index():
# 【提示1】 返回资源，资源为'Hello,World'
    return "小朋友 你是否有很多问号为什么 别人在那看漫画我却在学画画 对着钢琴说话别人在玩游戏我却靠在墙壁背我的 ABC我说我要一台大大的飞机但却得到一台旧旧录音机......"
# 【提示2】定义路由，资源地址为'/welcome'
@app.route('/welcome')
def welcome():
# 【提示2】返回资源，需要使用render_template方法，返回的网页为'welcome.html'
    return  render_template('welcome.html')


if __name__ == '__main__':
    app.run(port=5001,debug=True)


