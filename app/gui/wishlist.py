from flask import Blueprint, render_template, g

wish = Blueprint('wish_gui', __name__)


@wish.route('/wishlist', methods=['GET'])
def get_status():
    return render_template('wishlist.html', username=g.user)
