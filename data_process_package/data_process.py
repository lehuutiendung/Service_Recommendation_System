import json
import pandas
import csv 
from pandas import read_csv

# Ghi file .csv -> .txt
def convert_file_data_post(text):
    # Đọc file csv
    data_csv = open(text, "r")
    # Bỏ qua dòng tiêu đề
    csv_reader = csv.reader(data_csv)
    next(csv_reader)
    data_csv = ''.join([i for i in data_csv])  
    # Thay ',' bởi '\t'
    data_csv = data_csv.replace(",", "\t")  
    # Ghi dữ liệu vào file
    with open(r'G:\SocialNetwork_RecommendationSystems\MachineLearning\dataset\post_data.txt', 'w+', encoding='utf-8') as f:
        f.write(data_csv)
        f.close()

# Đọc file csv bài viết dạng dataframe ['post_id', 'title', 'category']
def get_title_post(text):
    post_cols = ['title', 'category', 'post_id']
    posts = pandas.read_csv(text, sep ='\t', names = post_cols, encoding='latin-1')
    list_post_title = posts['title'].values
    return list_post_title
def get_category_post(text):
    post_cols = ['title', 'category', 'post_id']
    posts = pandas.read_csv(text, sep ='\t', names = post_cols, encoding='latin-1')
    list_post_category = posts['category'].values
    return list_post_category

# Ghi file .csv -> .txt
def convert_file_data(text):
    # Đọc file csv
    data_csv = open(text, "r")
    # Bỏ qua dòng tiêu đề
    csv_reader = csv.reader(data_csv)
    next(csv_reader)
    data_csv = ''.join([i for i in data_csv])  
    # Thay ',' bởi '\t'
    data_csv = data_csv.replace(",", "\t")  
    # Ghi dữ liệu vào file
    with open(r'G:\SocialNetwork_RecommendationSystems\MachineLearning\dataset\view_data.txt', 'w+', encoding='utf-8') as f:
        f.write(data_csv)
        f.close()

# Đọc file view_data -> txt -> dạng dataframe ['userID', 'post_id', 'user_rating']
def get_data_interactive(text):
    columns = ['userID', 'post_id', 'user_rating']
    data = pandas.read_csv(text, sep='\t', names=columns, encoding='latin-1')
    Y_data = data.values
    return Y_data

# Đọc data từ file json -> dataframe
def get_data_from_json(dataJSON):
    df = pandas.read_json(dataJSON, typ='frame')
    return df.values

# Convert data query từ database -> dataframe
def convert_data_toframe(dataJSON):
    df = pandas.DataFrame(eval(dataJSON))
    df = df.drop(["_id", "__v"], axis=1)
    # Đảo lại thứ tự cột dataframe đúng với model training
    df = df[['owner','post','reactType']]
    return df.values