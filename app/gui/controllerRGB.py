from flask import Blueprint, render_template

rgb = Blueprint('rgb_gui', __name__)


@rgb.route('/rgb', methods=['GET'])
def get_rgb():
    return render_template('controllerRGB.html')
