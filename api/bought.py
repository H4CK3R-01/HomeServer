import datetime
from flask import request, jsonify, Blueprint
from auth import basicAuth
from tools import execute_sql, prepare_sql

bought = Blueprint('bought', __name__)


@bought.route('/api/v1/resources/bought/all', methods=['GET'])
def bought_all():
    result = execute_sql("SELECT * FROM gekauft")
    return jsonify({'status': 200, 'data': result})


@bought.route('/api/v1/resources/bought', methods=['POST'])
@basicAuth.login_required
def add_bought():
    data = request.json

    beschreibung = data['beschreibung']
    link = data['link']
    bild = data['bild']
    preis = data['preis']
    anzahl = data['anzahl']

    if beschreibung == "":
        return jsonify({'status': 500, 'message': "Description missing"})
    if link == "":
        return jsonify({'status': 500, 'message': "Link missing"})
    if bild == "":
        return jsonify({'status': 500, 'message': "Image missing"})
    if preis == "":
        return jsonify({'status': 500, 'message': "Price missing"})
    if anzahl == "":
        return jsonify({'status': 500, 'message': "Number missing"})

    try:
        float(preis)
    except ValueError:
        return jsonify({'status': 500, 'message': "Price is no number"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    # TODO SQL Injection
    result = execute_sql("SELECT * FROM gekauft WHERE link = '" + link + "'")

    if len(result) == 0:
        datum = datetime.date.today().strftime("%Y")
        bought_id = prepare_sql("INSERT INTO gekauft (beschreibung, link, anzahl, bild, preis, jahr) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (beschreibung, link, anzahl, bild, preis, datum))

        return jsonify({'status': 200, 'message': "Successfully added id=" + str(bought_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})
