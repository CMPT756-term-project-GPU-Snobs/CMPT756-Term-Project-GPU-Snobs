"""
SFU CMPT 756
Sample STANDALONE application---playlist service.
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
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

PERCENT_ERROR = 50
# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}

bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # TODO: Implement list_all
    return {}

@bp.route('/<music_id>', methods=['GET'])
def get_song(music_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music", "objkey": music_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        PlaylistName = content['PlaylistName']
        SongTitles = [x.strip() for x in content['SongTitles'].split(",")]
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    playlist_id = str(uuid.uuid4())
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "playlist", "playlistid": playlist_id, "genre": "Rock", "playlist": ["song1", "song2"]},
        headers={'Authorization': headers['Authorization']})
    
    return (response.json())

# @bp.route('/<playlist_id>', methods=['DELETE'])
# def delete_playlist(playlist_id):
#     global database
#     if playlist_id in database:
#         del database[playlist_id]
#     else:
#         response = {
#             "Count": 0,
#             "Items": []
#         }
#         return app.make_response((response, 404))
#     return {}

# @bp.route('/addsong', methods=['PATCH'])
# def add_song():
#     global database
#     try:
#         content = request.get_json()
#         playlist_id = content['PlaylistName']
#         PlaylistName = database[playlist_id][0]
#         SongTitles = database[playlist_id][1]
#         SongTitles += [content['SongTitles']]
#     except Exception:
#         return app.make_response(
#             ({"Message": "Error reading arguments"}, 400)
#             )
#     database[playlist_id] = (PlaylistName, SongTitles)
#     response = {
#         "playlist_id": playlist_id
#     }
#     return response

# @bp.route('/deletesong', methods=['DELETE'])
# def delete_song():
#     global database
#     try:
#         content = request.get_json()
#         playlist_id = content['PlaylistName']
#         PlaylistName = database[playlist_id][0]
#         SongTitles = database[playlist_id][1]
#         SongTitles.remove(content['SongTitles'])
#     except Exception:
#         return app.make_response(
#             ({"Message": "Error reading arguments"}, 400)
#             )
#     database[playlist_id] = (PlaylistName, SongTitles)
#     response = {
#         "playlist_id": playlist_id
#     }
#     return response

# @bp.route('/test', methods=['GET'])
# def test():
#     # This value is for user scp756-221
#     if ('123' != ucode):
#         raise Exception("Test failed")
#     return {}


# @bp.route('/shutdown', methods=['GET'])
# def shutdown():
#     # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
#     return {}


app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)