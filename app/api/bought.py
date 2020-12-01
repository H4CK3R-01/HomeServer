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
    result = cursor.fetchall()
    return jsonify({'status': 200, 'data': result})


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
        return jsonify({'status': 200, 'message': "Successfully added id=" + str(bought_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})
