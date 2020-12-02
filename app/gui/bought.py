from flask import Blueprint, render_template, g

bought = Blueprint('bought_gui', __name__)


@bought.route('/bought', methods=['GET'])
def get_bought():
    return render_template('bought.html', username=g.user)
