from flask import Blueprint, render_template, g

index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
def start():
    return render_template('index.html', username=g.user)
