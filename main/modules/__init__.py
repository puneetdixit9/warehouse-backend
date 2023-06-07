from flask_restx import Api
from main.modules.warehouse_manpower.view import wmp_namespace

api = Api()
api.add_namespace(wmp_namespace)
