from flask import Flask, render_template, request
import ybc_trans

app = Flask(__name__)


# 路由：返回“翻译表单”页面
@app.route('/trans')
def trans():
    # ☆☆☆【提示】按照项目目录结构修改html文件路径
    return render_template('trans/trans.html')


# 路由：实现翻译功能，返回“翻译结果”页面
@app.route('/do_trans', methods=['GET'])
def do_trans():
    text = request.args['text']
    result = ''
    lang = request.args['lang']
    # 实现翻译
    if lang == '英译汉':
        result = ybc_trans.en2zh(text)
    elif lang == '汉译英':
        result = ybc_trans.zh2en(text)
    # ☆☆☆【提示】按照项目目录结构修改html文件路径
    return render_template('trans/trans.html', t_text=text, t_result=result)


if __name__ == '__main__':
    app.run(port=5001, debug=True)


