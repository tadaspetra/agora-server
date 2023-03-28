from flask import Flask, render_template
import json
from flask_cors import CORS

from utils import start_call, stop_call, start_transcription

app = Flask(__name__)
CORS(app)


@app.route('/',)
def endpoints():
    app_routes = ['/start-call',
                  '/stop-call/<sid>/<resource_id>', '/start-transcription']
    return json.dumps(app_routes)


@app.route('/start-call', methods=['GET', 'POST'])
def start_recording():
    resource_id, sid = start_call()
    context = {'sid': sid, "resource_id": resource_id}
    return json.dumps(context)


@app.route('/stop-call/<path:sid>/<path:resource_id>', methods=['GET', 'POST'])
def stop_recording(sid, resource_id):
    data = stop_call(resource_id, sid)
    context = {}
    return json.dumps(data)


@app.route('/start-transcription', methods=['GET', 'POST'])
def start_recording():
    data = start_transcription()
    context = data
    return json.dumps(context)


if __name__ == '__main__':
    app.run(debug=True)
