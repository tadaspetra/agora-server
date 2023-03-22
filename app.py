from flask import Flask, render_template
import json
from flask_cors import CORS

from utils import start_call, stop_call

app = Flask(__name__)
CORS(app)


@app.route('/')
def endpoints():
    app_routes = ['/start-call', '/end-call/<sid>/<resource_id>']
    return json.dumps(app_routes)


@app.route('/start-call')
def start_recording():
    resource_id, sid = start_call()
    context = {'sid': sid, "resource_id": resource_id}
    return json.dumps(context)


@app.route('/stop-call/<path:sid>/<path:resource_id>')
def stop_recording(sid, resource_id):
    data = stop_call(resource_id, sid)
    context = {}
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
