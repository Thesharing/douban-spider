# 工具类

import pymongo
def save_to_mongodb(result,mongodb_db,mongodb_table,mongodb_url = 'mongodb://localhost:27017/'):
    """
    :param result: 存储到MongoDB的数据
    :param mongodb_db: 数据库名
    :param mongodb_table: 表名名
    :param mongodb_url: 数据库连接
    :return:
    """
    client = pymongo.MongoClient(mongodb_url)
    db = client[mongodb_db]
    if db[mongodb_table].insert_many(result):
        print("存储到mongodb成功",result)
