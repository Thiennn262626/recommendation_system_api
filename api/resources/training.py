from torch.utils.data import DataLoader
from models.loader import Loader
from models.factorized import MatrixFactorization
import numpy as np
import torch
from models.base import Model
from flask_restful import Resource
from flask import jsonify, make_response
from api.dbs.redis import redis_instance


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

        # Optimizer
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        # Tạo một instance của Model
        my_model = Model(model)

        # Huấn luyện mô hình
        my_model.fit(train_loader, num_epochs, loss_fn, optimizer, cuda=cuda)

        trained_product_embeddings = my_model.item_factors.weight.data.cpu().numpy()
        # luu mo hinh
        # np.save("trained_product_embeddings.npy", trained_product_embeddings)
        redis_instance.set_redis_data(
            "trained_product_embeddings", trained_product_embeddings.tolist()
        )
        redis_instance.set_expiration_time("trained_product_embeddings", 60*60*24*7)
        return make_response(
            jsonify(
                {
                    "Number of unique users:": n_users,
                    "Number of unique products": n_items,
                    "trained_product_embeddings": trained_product_embeddings.tolist(),
                }
            ),
            200,
        )
