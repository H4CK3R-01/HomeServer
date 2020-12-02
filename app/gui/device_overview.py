from flask import Blueprint, render_template, g

device = Blueprint('device_gui', __name__)


@device.route('/device', methods=['GET'])
def get_device():
    return render_template('device_overview.html', username=g.user)
