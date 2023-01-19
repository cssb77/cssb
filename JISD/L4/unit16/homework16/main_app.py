from flask import Flask, render_template, request
import ybc_trans

# 创建Flask对象app
app = Flask(__name__)


# 路由：返回“翻译表单”页面
@app.route('/trans')
def trans():
    return render_template('trans.html', t_lang='英译汉')


# 路由：实现翻译功能，返回“翻译结果”页面
@app.route('/do_trans')
def do_trans():
    text = ''
    lang = ''
    result = ''
    # 【提示1】获取需要翻译的内容(数据名称："text")，并保存在变量text中
    text = request.args['text']
    # 【提示2】获取当前翻译类型(数据名称："lang")，并保存在变量lang中
    lang = request.args['lang']
    # 【提示3】根据当前翻译类型，对提交的内容进行翻译，并将翻译结果保存在变量result中
    if lang == '英译汉':
        result = ybc_trans.en2zh(text)
    else:
        result = ybc_trans.zh2en(text)
    return render_template('trans.html', t_text=text, t_result=result, t_lang=lang)


if __name__ == '__main__':
    app.run(port=5001,debug=True)