import flask
from flask_cors import CORS
from wishlist import wish
from bought import bought
from status import status
from controllerRGB import rgb

app = flask.Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return ''


app.register_blueprint(wish)
app.register_blueprint(bought)
app.register_blueprint(status)
app.register_blueprint(rgb)

app.run()
