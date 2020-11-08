import json
import datetime

import flask
import mysql.connector
from flask import request, jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return ''


@app.route('/api/v1/resources/wish/lists', methods=['GET'])
def wish_lists():
    result = execute_sql('SELECT DISTINCT liste FROM wunschliste')
    lists_dict = {}
    with open("list.config") as config:
        data = json.load(config)

    for s in result:
        s = s[0]
        if s in data["wishlist"]:
            lists_dict[s] = data["wishlist"][s]
        else:
            lists_dict[s] = s.capitalize()

    return jsonify({'status': 200, 'data': lists_dict})


@app.route('/api/v1/resources/wish/list/<string:wish_list>', methods=['GET'])
def wish_one_list(wish_list):
    # TODO SQL Injection
    result = execute_sql("SELECT * FROM wunschliste WHERE liste = '{}' ORDER BY wichtigkeit".format(wish_list))
    return jsonify({'status': 200, 'data': result})


@app.route('/api/v1/resources/wish/<string:wish_list>', methods=['POST'])
def add_wish(wish_list):
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
    result = execute_sql("SELECT * FROM wunschliste WHERE link = '" + link + "' AND liste = '" + wish_list + "'")

    if len(result) == 0:
        wish_id = prepare_sql(
            "INSERT INTO wunschliste (beschreibung, link, anzahl, bild, preis, liste) VALUES (%s, %s, %s, %s, %s, %s)",
            (beschreibung, link, anzahl, bild, preis, wish_list))

        return jsonify({'status': 200, 'message': "Successfully added id=" + str(wish_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})


@app.route('/api/v1/resources/wish/update/<int:wish_id>', methods=['POST'])
def update_wish(wish_id):
    data = request.json
    beschreibung = data['beschreibung']
    link = data['link']
    bild = data['bild']
    preis = data['preis']
    anzahl = data['anzahl']
    liste = data['liste']

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
    if liste == "":
        return jsonify({'status': 500, 'message': "List missing"})

    try:
        float(preis)
    except ValueError:
        return jsonify({'status': 500, 'message': "Price is no number"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    prepare_sql("UPDATE wunschliste SET beschreibung = %s, link = %s, anzahl = %s, bild = %s, preis = %s, liste = %s "
                "WHERE id = %s", (beschreibung, link, anzahl, bild, preis, liste, wish_id))
    return jsonify({'status': 200, 'message': "Successfully updated id=" + str(wish_id)})


@app.route('/api/v1/resources/wish/delete/<int:wish_id>', methods=['POST'])
def delete_wish(wish_id):
    prepare_sql("DELETE FROM wunschliste WHERE id = %s", (wish_id,))
    return jsonify({'status': 200, 'message': "Successfully removed id=" + str(wish_id)})


# BOUGHT
@app.route('/api/v1/resources/bought/all', methods=['GET'])
def bought_all():
    result = execute_sql("SELECT * FROM gekauft")
    return jsonify({'status': 200, 'data': result})


@app.route('/api/v1/resources/bought', methods=['POST'])
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


def execute_sql(sql):
    mydb = mysql.connector.connect(
        host="192.168.178.55",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def prepare_sql(sql, params):
    mydb = mysql.connector.connect(
        host="192.168.178.55",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor(prepared=True)
    cursor.execute(sql, params)
    mydb.commit()
    try:
        return cursor.lastrowid
    except AttributeError:
        return


app.run()
