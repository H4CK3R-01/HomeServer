import json
import socket

from flask import jsonify, Blueprint

from auth import basicAuth, verify_password

status = Blueprint('status', __name__)


@status.route('/api/v1/resources/status/ssh', methods=['GET'])
def ssh():
    return check_port('ubuntu.fritz.box', 22, 'ssh')


@status.route('/api/v1/resources/status/octoprint', methods=['GET'])
def octoprint():
    return check_port('3dprinter.fritz.box', 80, 'octoprint')


@status.route('/api/v1/resources/status/db', methods=['GET'])
def db():
    return check_port('ubuntu.fritz.box', 3306, 'db')


@status.route('/api/v1/resources/status/phpmyadmin', methods=['GET'])
def phpmyadmin():
    return check_port('ubuntu.fritz.box', 9002, 'phpmyadmin')


@status.route('/api/v1/resources/status/mqtt', methods=['GET'])
def mqtt():
    return check_port('ubuntu.fritz.box', 1883, 'mqtt')


@status.route('/api/v1/resources/status/portainer', methods=['GET'])
def portainer():
    return check_port('ubuntu.fritz.box', 9000, 'portainer')


@status.route('/api/v1/resources/status/pihole', methods=['GET'])
def pihole():
    return check_port('ubuntu.fritz.box', 9001, 'pihole')


@status.route('/api/v1/resources/status/iobroker', methods=['GET'])
def iobroker():
    return check_port('ubuntu.fritz.box', 9003, 'iobroker')


@status.route('/api/v1/resources/status/tvheadend', methods=['GET'])
def tvheadend():
    return check_port('ubuntu.fritz.box', 9981, 'tvheadend')


@status.route('/api/v1/resources/status/raspap', methods=['GET'])
def raspap():
    return check_port('ubuntu.fritz.box', 9006, 'raspap')


@status.route('/api/v1/resources/status/website', methods=['GET'])
def website():
    return check_port('ubuntu.fritz.box', 80, 'website')


@status.route('/api/v1/resources/status/api', methods=['GET'])
def api():
    return check_port('ubuntu.fritz.box', 9005, 'api')


@status.route('/api/v1/resources/status/all', methods=['GET'])
def all_services():
    data = {
        'ssh': json.loads(ssh()),
        'octoprint': json.loads(octoprint()),
        'db': json.loads(db()),
        'phpmyadmin': json.loads(phpmyadmin()),
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


def check_port(host, port, name):
    if hasattr(basicAuth.get_auth(), 'username'):
        auth = verify_password(basicAuth.get_auth().username, basicAuth.get_auth().password)
    else:
        auth = False

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

    if auth:
        with open("list.config") as config:
            config_data = json.load(config)

        if name in config_data['credentials']:
            data['user'] = config_data["credentials"][name]["user"]
            data['password'] = config_data["credentials"][name]["password"]

    return json.dumps(data)


def generate_json(host, port, auth):
    if auth:
        return jsonify({'status': 200, 'user': 'admin', 'password': '12345678', 'data': check_port(host, port)})
