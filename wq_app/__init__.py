from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wqadmin:gobbldeygook@localhost/water_quality_ng'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import api definitions here because we need db already referenced
from wq_app.framework.views import SampleApi, FactorApi, ContaminantApi

# create db
db.create_all()

# create API and bind to app & db
api = Api(app)

# Setup api routing
api.add_resource(
    ContaminantApi,
    '/api/contaminant',
    '/api/contaminant/<int:contaminant_id>'
)

api.add_resource(
    SampleApi,
    '/api/sample',
    '/api/sample/<int:sample_id>'
)

api.add_resource(
    FactorApi,
    '/api/factor',
    '/api/factor/<int:factor_id>'
)


