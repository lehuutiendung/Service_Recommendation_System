########################################################################################################################
#
# File main train model
#
########################################################################################################################

import gui_program.gui
import data_process_package.data_process
import recommender_package.collab_filtering_train
import pandas as pd
import sys
import json
from bson.json_util import dumps
from pymongo import MongoClient
import numpy as np

client = MongoClient('localhost:27017')
db = client.socialnetwork_recommendation_db

if __name__ == "__main__":
    # reacts = db.reacts.find()
    # data_matrix = data_process_package.data_process.convert_data_toframe(dumps(reacts))
    
    data_matrix = data_process_package.data_process.get_data_from_json("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/view_data.json")

    cf_result = recommender_package.collab_filtering_train.CollabFiltering(data_matrix, k=2, uuCF=1)
    cf_result.fit()

    rate_test = np.asmatrix(data_matrix)
    n_tests = rate_test.shape[0]
    SE = 0 # squared error
    for n in range(n_tests):
        pred = cf_result.pred(rate_test[n, 0], rate_test[n, 1], normalized = 0)
        SE += (pred - rate_test[n, 2])**2 

    RMSE = np.sqrt(SE/n_tests)
    print("User-user CF, RMSE =", RMSE)

    list_result = cf_result.recommend_top(1, 10)
    # print(list_result)
    
    # list_post_title = data_process_package.data_process.get_title_post("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/post_data.txt")
    # list_post_category = data_process_package.data_process.get_category_post("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/post_data.txt")
    # gui_program.gui.main(cf_result, list_post_title, list_post_category)
    