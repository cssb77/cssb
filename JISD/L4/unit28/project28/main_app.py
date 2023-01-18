from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# 定义函数：查询家庭成员
def family_find(data):
    client = pymongo.MongoClient()
    db_ybc = client['ybc']
    c_family = db_ybc['family']
    family_list = []
    family = c_family.find(data)
    for i in family:
        family_list.append(i)
    return family_list


# 路由：返回“家庭成员页面
@app.route('/list')
def list():
    data = ['猿爸爸', '猿妈妈', '壮猿', '猿小花', '猿爷爷', '猿奶奶']
    return render_template('list.html', t_data=data)


# 路由：返回“家庭成员详细信息页面
@app.route('/dict')
def dict():
    data = family_find({})
    return render_template('dict.html', t_data=data)



if __name__ == '__main__':
    app.run(port=5001, debug=True)


