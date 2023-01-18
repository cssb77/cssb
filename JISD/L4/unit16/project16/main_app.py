from flask import Flask, render_template, request
import ybc_trans

app = Flask(__name__)


# 路由：返回“翻译表单”页面
@app.route('/')
def trans():
    return render_template('trans.html')


# 路由：返回“翻译结果”页面
@app.route('/do_trans', methods=['GET'])
def do_trans():
    text = request.args['text']
    result = ''
    # 【提示3】获取当前翻译类型"lang"，并保存在变量lang中
    00000
    # 【提示3】根据当前翻译类型，对提交的内容进行翻译，并将翻译结果保存在变量result中
    00000
    return render_template('trans.html', t_text=text, t_result=result)


if __name__ == '__main__':
    app.run(port=5001, debug=True)


