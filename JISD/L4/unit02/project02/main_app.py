from flask import Flask

app = Flask(__name__)

@app.route('/')
def demo():
    return 'Hello World！'

@app.route('/1')
def info():
    return '冲鸭！Level4！'

if __name__ == '__main__':
    app.run(debug=True, port=5001)