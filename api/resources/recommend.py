from flask import jsonify, make_response, request
from flask_restful import Resource
from api.dbs.redis import redis_instance

class RecommendByUser(Resource):
    def get(self):
        try:
            user_id = request.args.get("user_id", None)
            if user_id is None:
                return make_response(jsonify({"message": "User ID is required"}), 400)
            else:
                idx2userid_label = redis_instance.get_redis_data("userid2label")
                label_user = int(idx2userid_label[user_id])
                most_5star_productId_user_i = redis_instance.get_redis_data(
                   f'most_5star_productId_user_{label_user}'
                )
                if most_5star_productId_user_i is None:
                    return make_response(
                        jsonify(
                            {
                                "recommended_product": "No recommended product for this user",
                            }
                        ),
                        200,
                    )
                else:
                    return make_response(
                        jsonify(
                            {
                                "result": most_5star_productId_user_i,
                                "total": len(most_5star_productId_user_i),
                            }
                        ),
                        200,
                    )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
