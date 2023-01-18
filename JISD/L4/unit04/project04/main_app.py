from flask import Flask

app = Flask(__name__)


@app.route('/nae')
def name():
    return jiyuxiang
@app.route('/age')
def age():
    return 11
@app.route('/1')
def 1():
    return hhh
@app.route('/1/1/')
def 21():
    return 22222


if __name__ == '__main__':
