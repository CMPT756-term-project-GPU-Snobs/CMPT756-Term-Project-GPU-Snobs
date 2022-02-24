"""
SFU CMPT 756
Sample STANDALONE application---music service.
"""

# Standard library modules
import csv
import logging
import os
import sys
import uuid
import json

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request

#SAMPLE DATABASE CREATION
# The path to the file (CSV format) containing the sample data
DB_PATH = './data/music.csv'

if not os.path.isdir('data'):
    os.mkdir('data')

# with open(DB_PATH, mode='a') as f: 
#     if os.path.getsize(DB_PATH) == 0:
#         f.write("Artist,SongTitle,UUID\n")

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
ucode = '123'

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}

def load_db():
    global database
    with open('./data/playlists.json', 'r') as f:
        rdr = json.load(f)
        for id, data in rdr.items():
            print("here")
            playlist_name, songs = data
            database[id] = (playlist_name, songs)


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/', methods=['GET'])
def list_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'PlaylistName': value[0], 'SongTitles': value[1], 'playlist_id': id}
             for id, value in database.items()]
    }
    return response


@bp.route('/<playlist_id>', methods=['GET'])
def get_song(playlist_id):
    global database
    if playlist_id in database:
        value = database[playlist_id]
        response = {
            "Count": 1,
            "Items":
                [{'PlaylistName': value[0],
                  'SongTitles': value[1],
                  'playlist_id': playlist_id}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/', methods=['POST'])
def create_song():
    global database
    try:
        content = request.get_json()
        PlaylistName = content['PlaylistName']
        SongTitles = content['SongTitles']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    playlist_id = str(uuid.uuid4())
    database[playlist_id] = (PlaylistName, SongTitles)
    response = {
        "playlist_id": playlist_id
    }
    return response


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_song(playlist_id):
    global database
    if playlist_id in database:
        del database[playlist_id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}


@bp.route('/test', methods=['GET'])
def test():
    # This value is for user scp756-221
    if ('123' != ucode):
        raise Exception("Test failed")
    return {}


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/music/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    load_db()
    app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)