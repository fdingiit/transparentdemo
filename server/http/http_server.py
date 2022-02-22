import sys

from flask import Flask, request, jsonify

app = Flask(__name__)

port = 80


@app.route('/')
def hello():
    return jsonify({
        'server_port': port,
        'client_addr': request.remote_addr,
        'client_port': request.environ.get('REMOTE_PORT'),
    })


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
