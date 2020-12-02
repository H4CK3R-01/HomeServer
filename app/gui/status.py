from flask import Blueprint, render_template, g

status = Blueprint('status_gui', __name__)


@status.route('/status', methods=['GET'])
def get_status():
    return render_template('status.html', username=g.user)
