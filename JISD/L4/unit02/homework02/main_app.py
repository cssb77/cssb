from flask import Flask

app = Flask(__name__)

@app.route('/')
def demo():
    return '我在猿编程学习编程！'

@app.route('/24/6')
def info():
    return '已经学到Level4啦！'





if __name__ == '__main__':
    app.run(debug=True, port=5001)