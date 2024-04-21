from flask import Blueprint
from flask_restful import Api

from api.resources.training import Training
from api.resources.recommend import RecommendByUser
from api.resources.recommendbyproduct import RecommendByProduct

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, errors=blueprint.errorhandler)


@blueprint.errorhandler(404)
def page_not_found(e):
    return {'message': 'Resource not found'}, 404


@blueprint.errorhandler(500)
def server_error(e):
    return {'message': 'Server error'}, 500

@blueprint.errorhandler(400)
def bad_request(e):
    return {'message': 'Bad request'}, 400

api.add_resource(Training, '/training')
api.add_resource(RecommendByUser, '/recommend-by-user')
api.add_resource(RecommendByProduct, '/recommend-by-product')



