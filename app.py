from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (
        'root',
        '123456',
        '127.0.0.1',
        3306,
        'statistics')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['extend_existing'] = True

db = SQLAlchemy(app)

import models



@app.route('/')
def hello_world():
    return 'Hello World!'

def init_app():
    return models.init_db()


if __name__ == '__main__':

    app.run()
