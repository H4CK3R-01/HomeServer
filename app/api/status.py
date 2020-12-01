import json
import os
import socket

from flask import jsonify, Blueprint, g

status = Blueprint('status', __name__, url_prefix='/api/v1/resources/status')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@status.route('/ssh', methods=['GET'])
def ssh():
    return check_port('server.fritz.box', 22, 'ssh')


@status.route('/octoprint', methods=['GET'])
def octoprint():
    return check_port('3dprinter.fritz.box', 80, 'octoprint')


@status.route('/db', methods=['GET'])
def db():
    return check_port('server.fritz.box', 3306, 'db')


@status.route('/phpmyadmin', methods=['GET'])
def phpmyadmin():
    return check_port('server.fritz.box', 9002, 'phpmyadmin')


@status.route('/api/v1/resources/status/mqtt', methods=['GET'])
def mqtt():
    return check_port('server.fritz.box', 1883, 'mqtt')


@status.route('/portainer', methods=['GET'])
def portainer():
    return check_port('server.fritz.box', 9000, 'portainer')


@status.route('/pihole', methods=['GET'])
def pihole():
    return check_port('server.fritz.box', 9001, 'pihole')


@status.route('/iobroker', methods=['GET'])
def iobroker():
    return check_port('server.fritz.box', 9003, 'iobroker')


@status.route('/tvheadend', methods=['GET'])
def tvheadend():
    return check_port('server.fritz.box', 9981, 'tvheadend')


@status.route('/raspap', methods=['GET'])
def raspap():
    return check_port('server.fritz.box', 9006, 'raspap')


@status.route('/website', methods=['GET'])
def website():
    return check_port('server.fritz.box', 80, 'website')


@status.route('/api', methods=['GET'])
def api():
    return check_port('server.fritz.box', 9005, 'api')


@status.route('/all', methods=['GET'])
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
    auth = False
    if g.user is not None:
        auth = True

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
        with open(os.path.join(__location__, '../list.config')) as config:
            config_data = json.load(config)

        if name in config_data['credentials']:
            data['user'] = config_data["credentials"][name]["user"]
            data['password'] = config_data["credentials"][name]["password"]

    return json.dumps(data)
