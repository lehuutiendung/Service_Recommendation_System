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
    # 70% tập train
    data_matrix_train = data_process_package.data_process.get_data_from_json("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/Train/view_data_train.json")
    # 30% tập test
    data_matrix_test = data_process_package.data_process.get_data_from_json("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/Test/view_data_test.json")

    rate_train = np.asmatrix(data_matrix_train)
    rate_test = np.asmatrix(data_matrix_test)

    n_tests = rate_test.shape[0]

    # User - user
    cf_result = recommender_package.collab_filtering_train.CollabFiltering(data_matrix_train, k=2, uuCF=1)
    cf_result.fit()

    # # Item - item
    # cf_result = recommender_package.collab_filtering_train.CollabFiltering(data_matrix_train, k=2, uuCF=0)
    # cf_result.fit()

    SE = 0 #error
    SE_MAE = 0 #Absolute error
    for n in range(n_tests):
        pred = cf_result.pred(rate_test[n, 0], rate_test[n, 1], normalized = 0)
        SE += (pred - rate_test[n, 2])**2 
        SE_MAE += (pred - rate_test[n, 2])

    MAE = np.sqrt(SE_MAE/n_tests)
    MSE = (SE/n_tests)
    RMSE = np.sqrt(MSE)
    print("CF, MAE =", MAE)
    print("CF, MSE =", MSE)
    print("CF, RMSE =", RMSE)
    
    # list_post_title = data_process_package.data_process.get_title_post("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/post_data.txt")
    # list_post_category = data_process_package.data_process.get_category_post("G:/SocialNetwork_RecommendationSystems/RecommendWebAPI/dataset/post_data.txt")
    # gui_program.gui.main(cf_result, list_post_title, list_post_category)
    