from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zfadmin:gobbldeygook@localhost/water_quality'
db = SQLAlchemy(app)


if __name__=='__main__':
    print('Water Quality API Starting Up...')