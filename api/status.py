import json
import socket

from flask import jsonify, Blueprint

status = Blueprint('status', __name__)


@status.route('/api/v1/resources/status/ssh', methods=['GET'])
def ssh():
    return check_port('ubuntu.fritz.box', 22)


@status.route('/api/v1/resources/status/octoprint', methods=['GET'])
def octoprint():
    return check_port('3dprinter.fritz.box', 80)


@status.route('/api/v1/resources/status/db', methods=['GET'])
def db():
    return check_port('ubuntu.fritz.box', 3306)


@status.route('/api/v1/resources/status/mqtt', methods=['GET'])
def mqtt():
    return check_port('ubuntu.fritz.box', 1883)


@status.route('/api/v1/resources/status/portainer', methods=['GET'])
def portainer():
    return check_port('ubuntu.fritz.box', 9000)


@status.route('/api/v1/resources/status/pihole', methods=['GET'])
def pihole():
    return check_port('ubuntu.fritz.box', 9001)


@status.route('/api/v1/resources/status/iobroker', methods=['GET'])
def iobroker():
    return check_port('ubuntu.fritz.box', 9003)


@status.route('/api/v1/resources/status/tvheadend', methods=['GET'])
def tvheadend():
    return check_port('ubuntu.fritz.box', 9981)


@status.route('/api/v1/resources/status/raspap', methods=['GET'])
def raspap():
    return check_port('ubuntu.fritz.box', 80)


@status.route('/api/v1/resources/status/website', methods=['GET'])
def website():
    return check_port('ubuntu.fritz.box', 80)


@status.route('/api/v1/resources/status/api', methods=['GET'])
def api():
    return check_port('ubuntu.fritz.box', 80)


@status.route('/api/v1/resources/status/all', methods=['GET'])
def all_services():
    data = {
        'ssh': json.loads(ssh()),
        'octoprint': json.loads(octoprint()),
        'db': json.loads(db()),
        'mqtt': json.loads(mqtt()),
        'portainer': json.loads(portainer()),
        'pihole': json.loads(pihole()),
        'iobroker': json.loads(iobroker()),
        'tvheadend': json.loads(tvheadend()),
        'raspap': json.loads(raspap()),
        'website': json.loads(website()),
        'api': json.loads(api())
    }
    return jsonify({'status': 200, 'data': data})


def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    data = {
        'port': port,
        'host': host,
        'open': True
    }
    if result == 0:
        data['open'] = True
    else:
        data['open'] = False
    sock.close()
    return json.dumps({'status': 200, 'data': data})
