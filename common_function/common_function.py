from bson.json_util import dumps
from pymongo import MongoClient
from bson.dbref import DBRef

client = MongoClient('localhost:27017')
db = client.socialnetwork_recommendation_db

def getListPost(userIDMongo, listID, top_x):
    result = []
    count = 0
    for postID in listID:
        post = db.posts.find_one({"postID": postID})
        
        if post is None:
            continue
        else:
            # Loại bỏ các bài viết của người dùng hiện tại ra khỏi list gợi ý
            userIDMongoStr = str(post["owner"])
            if userIDMongoStr == userIDMongo: continue

        userRef = db.users.find_one({"_id": post["owner"]}, {"userName": 1, "avatar": 1})
        post["owner"] = userRef
        result.append(post)
        # Lấy đủ số lượng top_x bài recommend
        count = count + 1
        if(count == top_x):
            break
    return result