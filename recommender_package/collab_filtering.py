import numpy as np
from scipy.fft import idst
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.socialnetwork_recommendation_db

# Class xây dựng hệ gợi ý dựa trên sự tương đồng giữa user-user, item-item
class CollabFiltering(object):
    def __init__(self, data_matrix, k, dist_funct=cosine_similarity, uuCF=1):
    # Hàm khởi tạo với các tham số đầu vào:
    #   data_matrix: ma trận tiện ích (Utility Matrix) -> 3 cột: user_id, post_id, rating
    #   k: số láng giềng được lựa chọn để dự đoán 
    #   dist_funct: Hàm khoảng cách, tương đồng -> Sử dụng hàm cosine_similarity của thư viện sklearn
    #   uuCF: Sử dụng tương đồng user-user là 1, sử dụng item-item là 0. Mặc định sử dụng user-user collaborative filtering
        self.uuCF = uuCF  
        self.Y_data = data_matrix if uuCF == 1 else data_matrix[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_funct
        self.Ybar_data = None           #Khởi tạo ma trận Y ngang (Ma trận chuẩn hóa)
        # số lượng user và item
        # xác định số user, item trong matrix Y9
        doc_maxUserID = db.users.find_one(sort=[('userID',-1)])
        doc_maxPostID = db.posts.find_one(sort=[('postID',-1)])
        # self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        # self.n_items = int(np.max(self.Y_data[:, 1])) + 1
        self.n_users = doc_maxUserID["userID"] + 1
        self.n_items = doc_maxPostID["postID"] + 1

    ###
    # Chuẩn hóa ma trận
    def normalize_matrix(self):
        userIDs = self.Y_data[:, 0]
        self.avg_rating = np.zeros((self.n_users,))
        self.Ybar_data = self.Y_data.copy().astype(np.float32)     

        for i in range(self.n_users):
            # Mảng index bản ghi của cùng một user
            ids = np.where(userIDs == i)[0].astype(np.int32)
            # Mảng item mà user đánh giá
            item_ids = self.Y_data[ids, 1]
            ratings = self.Y_data[ids, 2]
            # Lấy giá trị trung bình rating của một user
            tmp = np.mean(ratings)
            if np.isnan(tmp):
                tmp = 0  # để tránh mảng trống và nan value, default rating trung bình = 0 đối với isNAN
            self.avg_rating[i] = tmp
            # chuẩn hóa
            self.Ybar_data[ids, 2] = (ratings.astype(float)- self.avg_rating[i])
        # Ma trận Y ngang (đại diện cho ma trận chuẩn hóa)
        self.Ybar = sparse.coo_matrix(( self.Ybar_data[:, 2], 
                                        (self.Ybar_data[:, 1], self.Ybar_data[:, 0])
                                      ), (self.n_items, self.n_users), dtype=np.float32)
        self.Ybar = self.Ybar.tocsr()

    ###
    # Tính toán ma trận tương đồng
    def similarity_matrix(self):
        self.Similar = self.dist_func(self.Ybar.T, self.Ybar.T)
    ##
    # Chuẩn hóa dữ liệu và tính toán lại ma trận similarity. (sau khi một số xếp hạng được thêm vào).
    def refresh(self):
        self.normalize_matrix()
        self.similarity_matrix()
    
    def fit(self):
        self.refresh()

    ###
    # Dự đoán rating
    def __pred(self, u, i, normalized=1):
        # Tìm tất cả user đã rate item i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        sim = self.Similar[u, users_rated_i]
        a = np.argsort(sim)[-self.k:]
        nearest_s = sim[a]
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            # Cộng với 1e-8, để tránh chia cho 0
            return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)
        return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.avg_rating[u]

    ###
    # Xác định phương pháp uuCF hoặc iiCF
    def pred(self, u, i, normalized=1):
        if self.uuCF: return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend_top(self, u, top_x):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        item = {'id': None, 'similar': None}
        list_items = []
        
        def take_similar(elem):
            return elem['similar']

        for i in range(self.n_items):
            # i không nằm trong list item đã được đánh giá, i khác 0 (vì min ID = 1)
            if (i not in items_rated_by_u and i != 0):
                rating = self.__pred(u, i)
                item['id'] = i
                item['similar'] = rating
                list_items.append(item.copy())

        sorted_items = sorted(list_items, key=take_similar, reverse=True)
        return sorted_items