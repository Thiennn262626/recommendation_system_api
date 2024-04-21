from flask import jsonify, make_response, request
from flask_restful import Resource
from api.dbs.redis import redis_instance
import numpy as np

class RecommendByProduct(Resource):
    def get(self):
        try:
            product_id = request.args.get("product_id", None)
            if product_id is None:
                return make_response(jsonify({"message": "Product ID is required"}), 400)
            else:
                productid2idx = redis_instance.get_redis_data("productid2idx")
                product_index = productid2idx[product_id]
                product_embedding = redis_instance.get_redis_data("trained_product_embeddings")
                product_vector = product_embedding[product_index]
                distances_x = [np.linalg.norm(np.array(v) - np.array(product_vector)) for v in product_embedding]
                top60_product_index = np.argsort(distances_x)[1:61]
                # chuyen index sang id dua tren value cua productid2idx
                top60_product_id = [list(productid2idx.keys())[list(productid2idx.values()).index(i)] for i in top60_product_index]

                return make_response(
                    jsonify(
                        {
                            "result": top60_product_id,
                            "total": len(top60_product_id),
                        }
                    ),
                    200,
                )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)