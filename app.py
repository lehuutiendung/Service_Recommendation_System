from ast import Try
from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
import data_process_package.data_process
import recommender_package.collab_filtering
import common_function.common_function
import sys 
import numpy as np

client = MongoClient('localhost:27017')
db = client.socialnetwork_recommendation_db

app = Flask(__name__)
CORS(app)

@app.route("/test")
def hello():
    return "Test API Python"

# Lấy tất cả bản ghi tương tác của người dùng - bài viết
@app.route("/api/recommends/recommend-post", methods = ['POST'])
def get_react():
    try:
        # Lấy data request từ raw body
        res_data = request.get_json()
        userID = res_data['userID']
        userIDMongo = res_data['userIDMongo']
        
        # Lấy dữ liệu tương tác người dùng - bài viết từ database
        reacts = db.reacts.find()
        data_matrix = data_process_package.data_process.convert_data_toframe(dumps(reacts))
        cf_result = recommender_package.collab_filtering.CollabFiltering(data_matrix, k=2, uuCF=1)
        cf_result.fit()

        # Đánh giá
        # rate_test = np.asmatrix(data_matrix)
        # n_tests = rate_test.shape[0]
        # SE = 0 # squared error
        # for n in range(n_tests):
        #     pred = cf_result.pred(rate_test[n, 0], rate_test[n, 1], normalized = 0)
        #     SE += (pred - rate_test[n, 2])**2 

        # RMSE = np.sqrt(SE/n_tests)
        # print(SE)
        # print(n_tests)
        # print("User-user CF, RMSE =", RMSE)

        #Lấy top x recommend
        top_x = 5
        list_result = cf_result.recommend_top(userID, top_x)
        listPostID = []
        for i in list_result:
            listPostID.append(i["id"])
        lst_post_result = common_function.common_function.getListPost(userIDMongo, listPostID, top_x)
        return dumps(lst_post_result)
    except Exception as e:
        return dumps({'error' : str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    app.run(host=host, port=port)
    # run with nodemon: nodemon --exec python app.py 