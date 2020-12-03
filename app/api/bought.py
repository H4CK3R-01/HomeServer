import datetime

from flask import request, jsonify, Blueprint

from app.auth import login_required
from app.db import get_db

bought = Blueprint('bought', __name__, url_prefix='/api/v1/resources/bought')


@bought.route('/', methods=['GET'])
def bought_all():
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM gekauft')
    data = jsonify({'data': cursor.fetchall()})
    return data


@bought.route('/', methods=['POST'])
@login_required
def add_bought():
    data = request.json

    beschreibung = data['beschreibung']
    link = data['link']
    bild = data['bild']
    preis = data['preis']
    anzahl = data['anzahl']

    if beschreibung == "":
        return jsonify({'message': "Description missing"}), 422
    if link == "":
        return jsonify({'message': "Link missing"}), 422
    if bild == "":
        return jsonify({'message': "Image missing"}), 422
    if preis == "":
        return jsonify({'message': "Price missing"}), 422
    if anzahl == "":
        return jsonify({'message': "Number missing"}), 422

    try:
        float(preis)
    except ValueError:
        return jsonify({'message': "Price is no number"}), 422

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'message': "Number is no integer"}), 422

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM gekauft WHERE link = ?', (link, ))
    result = cursor.fetchall()

    if len(result) == 0:
        datum = datetime.date.today().strftime("%Y")
        cursor.execute('INSERT INTO gekauft (beschreibung, link, anzahl, bild, preis, jahr) '
                       'VALUES (?, ?, ?, ?, ?, ?)', (beschreibung, link, anzahl, bild, preis, datum))
        bought_id = cursor.lastrowid
        db.commit()
        return jsonify({'message': "Successfully added id=" + str(bought_id)})
    else:
        return jsonify({'message': "Already in list"}), 422
