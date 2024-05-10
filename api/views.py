from flask import Blueprint
from flask_restful import Api

from api.resources.training import Training
from api.resources.recommend import RecommendByUser
from api.resources.recommendbyproduct import RecommendByProduct

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, errors=blueprint.errorhandler)

api.add_resource(Training, '/training')
# api.add_resource(RecommendByUser, '/recommend-by-user')
# api.add_resource(RecommendByProduct, '/recommend-by-product')



