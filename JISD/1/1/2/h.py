import pymongo
def jiq(q,w,ji1):
    ab_ji = client[q]
    c_ji = ab_ji[w]
    c_ji.insert_one({'1': ji1})

jiq('ji','ji','{1;qq}')
