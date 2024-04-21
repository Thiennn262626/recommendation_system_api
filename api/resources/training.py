from torch.utils.data import DataLoader
from models.loader import Loader
from models.factorized import MatrixFactorization
import numpy as np
import torch
from sklearn.cluster import KMeans
from models.base import Model
from flask_restful import Resource
from flask import jsonify, make_response
from api.dbs.redis import redis_instance
import json


class Training(Resource):
    def get(self):
        num_epochs = 128
        cuda = torch.cuda.is_available()
        train_set = Loader()
        train_loader = DataLoader(train_set, batch_size=128, shuffle=True)
        n_users = len(train_set.userid2idx.keys())
        n_items = len(train_set.productid2idx.keys())
        model = MatrixFactorization(n_users, n_items, n_factors=8)
        # Loss function
        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
        my_model = Model(model)
        # Huấn luyện mô hình
        my_model.fit(train_loader, num_epochs, loss_fn, optimizer, cuda=cuda)
        # Ket qua sau khi train
        trained_product_embeddings = my_model.item_factors.weight.data.cpu().numpy()
        trained_user_embeddings = my_model.user_factors.weight.data.cpu().numpy()
        # luu mo hinh vao redis
        redis_instance.set_redis_data(
            "trained_product_embeddings", trained_product_embeddings.tolist(), 3600
        )
        # kmeans_product = KMeans(n_clusters=4, random_state=0).fit(
        #     trained_product_embeddings
        # )
        kmeans_user = KMeans(n_clusters=4, random_state=0).fit(trained_user_embeddings)

        # gan label cho user
        for i, key in enumerate(train_set.userid2idx):
            train_set.userid2idx[key] = int(kmeans_user.labels_[i])
        redis_instance.set_redis_data("userid2label", train_set.userid2idx, 3600)
        # tim san pham dac trung cua moi cluster user, san pham nao duoc danh gia 5 sao nhieu nhat
        for i, key in enumerate(train_set.userid2idx):
            train_set.idx2userid[i] = int(kmeans_user.labels_[i])
        rating_df = train_set.ratings
        rating_df.userId = rating_df.userId.apply(lambda x: train_set.idx2userid[x])
        for i in range(4):
            rating_df_cluster = rating_df[
                (rating_df["userId"] == i) & (rating_df["rating"] >= 4)
            ]
            # Đếm số lượng đánh giá 5* cho mỗi productId
            count_5star = rating_df_cluster.groupby("productId").size()
            # Sắp xếp kết quả theo số lượng đánh giá giảm dần
            sorted_count_5star = count_5star.sort_values(ascending=False)
            # Lấy ra all productId có số lượng đánh giá 5* nhiều nhất
            most_5star_productId = sorted_count_5star.index.to_list()
            # doi tu index sang id ban dau
            most_5star_productId = [
                train_set.idx2productid[i] for i in most_5star_productId
            ]
            redis_instance.set_redis_data(
                f"most_5star_productId_user_{i}",
                most_5star_productId[:10],
                3600,
            )
        return make_response(
            jsonify(
                {
                    "Number of unique users:": n_users,
                    "Number of unique products": n_items,
                }
            ),
            200,
        )
