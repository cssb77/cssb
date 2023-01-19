# 获取表单提交的排名，根据排名查询数据
# 返回页面及数据，在页面中显示查询到的信息及宠物狗图片

from flask import Flask,render_template,request
import pymongo


app = Flask(__name__)
def dog_find(data):
    client = pymongo.MongoClient()
    db_pet = client['pet']
    c_dog = db_pet['dog']
    dog_list = []
    res = c_dog.find(data)
    for i in res:
        dog_list.append(i)
    print('OK')
    return dog_list


@app.route('/find')
def find():
    return render_template('find.html')

@app.route('/res')
def res():
    # 【提示1】获取表单提交的排名信息
    # 【提示1】从args字典中获取'num'键对应的值，保存在变量num中
    num = request.args['num']
    # 【提示2】使用函数，查询对应排名的数据
    # 【提示2】将排名信息字典作为参数，传入到函数dog_find()中，获取数据列表，保存到变量res中
    res = dog_find({'num':num})

    # 【提示3】获取对应的图片路径
    # 【提示3】从列表res中，根据索引定位到字典数据，再获取'img'键对应的值，保存到变量img中
    img = res[0]['img']
    # 显示页面及数据
    return render_template('res.html',t_res=res,t_img=img)

if __name__ == '__main__':
    app.run(port=5001,debug=True)





