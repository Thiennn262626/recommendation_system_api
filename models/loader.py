from torch.utils.data.dataset import Dataset
import pandas as pd
import torch
from api.controllers.ratings import RatingList
from api.dbs.redis import redis_instance

# Note: This isn't 'good' practice, in a MLops sense but we'll roll with this since the data is already loaded in memory.
class Loader(Dataset):
    def __init__(self):

        self.ratings = RatingList().get()
        ratings_df = self.ratings
        # Extract all user IDs and product IDs
        users = ratings_df.userId.unique()
        product = ratings_df.productId.unique()
        # --- Producing new continuous IDs for users and products ---
        # Unique values : index
        self.userid2idx = {o: i for i, o in enumerate(users)}
        self.productid2idx = {o: i for i, o in enumerate(product)}
        redis_instance.set_redis_data("productid2idx", self.productid2idx, 3600)
        self.idx2userid = {i: o for o, i in self.userid2idx.items()}
        self.idx2productid = {i: o for o, i in self.productid2idx.items()}

        self.ratings.productId = ratings_df.productId.apply(
            lambda x: self.productid2idx[x]
        )
        self.ratings.userId = ratings_df.userId.apply(lambda x: self.userid2idx[x])

        self.x = self.ratings.drop(["rating", "timestamp"], axis=1).values
        self.y = self.ratings["rating"].values
        self.x, self.y = torch.tensor(self.x), torch.tensor(
            self.y
        )  # Transforms the data to tensors (ready for torch models.)

    def __getitem__(self, index):
        return (self.x[index], self.y[index])

    def __len__(self):
        return len(self.ratings)
