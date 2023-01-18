from flask import Flask, render_template, request
import ybc_trans

app = Flask(__name__)


# 路由：返回“翻译表单”页面
@app.route('/trans')
def trans():
    # 【提示1】通过render_template方法返回"trans.html"
    return ''


# 路由：返回“翻译结果”页面
@app.route('/do_trans', methods=['GET'])
def do_trans():
    # 【提示2】获取数据名称"text"的值，并保存在变量text中
    text = request.args("text")
    # 【提示2】将变量text中的英语内容翻译为汉语，并将结果保存在变量result中
    00000
    # 【提示2】为模板变量t_result赋值
    # 【提示4】为模板变量t_text赋值
    return render_template('trans.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)


