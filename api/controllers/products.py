from flask_restful import Resource
import pandas as pd
from api.dbs.connection_hander import db_connection

class ProductList(Resource):
    def get(self):
        products = db_connection.fetch_data('SELECT id, name FROM [Product]')
        products_df = pd.DataFrame(products, columns=['productId', 'name'])
        return products_df
