from flask import jsonify, make_response, request
import numpy as np
import pandas as pd
from flask_restful import Resource
from api.dbs.redis import redis_instance
from sklearn.cluster import KMeans
from api.resources.training import Training


class Recommend(Resource):
    def get(self):
        try:
            # Get trained product embeddings
            trained_product_embeddings = redis_instance.get_redis_data(
                "trained_product_embeddings"
            )
            if trained_product_embeddings is None:
                print("Training model...")
                Training().get()
                trained_product_embeddings = redis_instance.get_redis_data(
                    "trained_product_embeddings"
                )
            else:
                trained_product_embeddings = np.array(trained_product_embeddings)

            # Get user ID from request query parameters
            user_id = request.args.get("user_id", None)

            if user_id is None:
                return make_response(jsonify({"message": "User ID is required"}), 400)
            else:
                rating_encoded = redis_instance.get_redis_data("ratings_encoded")
                if rating_encoded is None:
                    return make_response(
                        jsonify({"message": "Ratings data is not available"}), 500
                    )
                else:
                    rating_array = np.array(rating_encoded)
                    first_values_equal_to_1 = rating_array[
                        rating_array[:, 0] == user_id
                    ][0]
                    user_id = int(first_values_equal_to_1[4])

                    kmeans = KMeans(n_clusters=5, random_state=0).fit(
                        trained_product_embeddings
                    )

                    # Get cluster label based on user ID (this is just a dummy example)
                    cluster_label = user_id % 5
                    # Find products in the cluster
                    products_in_cluster = np.where(kmeans.labels_ == cluster_label)[0]
                    result = []
                    for i in products_in_cluster:
                        for j in rating_array:
                            if i == int(j[5]):
                                result.append(j[1])
                                break
                    return make_response(
                        jsonify({"recommended_product": result, 'total': len(result)}),
                        200,
                    )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
