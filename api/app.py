import flask
from flask_cors import CORS

from auth import auth, db
from bought import bought
from controllerRGB import rgb
from device_overview import dev
from status import status
from wishlist import wish

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yiQHZzmYOFvLJPXxWjIFIkNZKtVcXSDTDM70SGhKnBE526lW38GdbRARsNMeHgqraQ1uUpYL4PBfTAoJ9wCEVUOC'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin!123@ubuntu.fritz.box/mydb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return ''


app.register_blueprint(auth)
app.register_blueprint(wish)
app.register_blueprint(bought)
app.register_blueprint(status)
app.register_blueprint(rgb)
app.register_blueprint(dev)

db.init_app(app)

if __name__ == "__main__":
    app.run()
