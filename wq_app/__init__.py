from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand

from wq_app.framework.views import SampleApi, FactorApi, ContaminantApi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wqadmin:gobbldeygook@localhost/water_quality_ng'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create db
db.create_all()

# create API and bind to app
api = Api(app)

# Setup api routing
api.add_resource(
    ContaminantApi,
    '/api/contaminant',
    '/api/contaminant/<int:id>'
)

api.add_resource(
    SampleApi,
    '/api/sample',
    '/api/sample/<int:id>'
)

api.add_resource(
    FactorApi,
    '/api/factor',
    '/api/factor/<int:id>'
)


