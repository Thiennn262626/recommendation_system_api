from torch.utils.data.dataset import Dataset
import pandas as pd
import torch
from api.controllers.ratings import RatingList
from api.dbs.redis import redis_instance

# Note: This isn't 'good' practice, in a MLops sense but we'll roll with this since the data is already loaded in memory.
class Loader(Dataset):
    def __init__(self):

        self.ratings = RatingList().get()
        datacopy = self.ratings.copy()
        ratings_df = self.ratings
        # Extract all user IDs and product IDs
        users = ratings_df.userId.unique()
        product = ratings_df.productId.unique()
        # --- Producing new continuous IDs for users and products ---
        # Unique values : index
        self.userid2idx = {o: i for i, o in enumerate(users)}
        self.productid2idx = {o: i for i, o in enumerate(product)}
        # print("abc:2 ", self.userid2idx, self.productid2idx)
        # Obtained continuous ID for users and products
        self.idx2userid = {i: o for o, i in self.userid2idx.items()}
        self.idx2productid = {i: o for o, i in self.productid2idx.items()}
        # print("abc:3 ", self.idx2userid, self.idx2productid)
        # return the id from the indexed values as noted in the lambda function down below.
        self.ratings.productId = ratings_df.productId.apply(
            lambda x: self.productid2idx[x]
        )
        self.ratings.userId = ratings_df.userId.apply(lambda x: self.userid2idx[x])
        # luu lai du lieu sau khi encode de su dung cho viec recommend
        datacopy.rename(
            columns={"userId": "userId_original", "productId": "productId_original"},
            inplace=True,
        )
        dataconcat = pd.concat(
            [datacopy, self.ratings[["userId", "productId"]]], axis=1
        )
        print("dataconcat: ", dataconcat)
        redis_instance.set_redis_data("ratings_encoded", dataconcat.values.tolist())
        redis_instance.set_expiration_time("ratings_encoded", 60*60*24*7)

        self.x = self.ratings.drop(["rating", "timestamp"], axis=1).values
        self.y = self.ratings["rating"].values
        self.x, self.y = torch.tensor(self.x), torch.tensor(
            self.y
        )  # Transforms the data to tensors (ready for torch models.)

    def __getitem__(self, index):
        return (self.x[index], self.y[index])

    def __len__(self):
        return len(self.ratings)
