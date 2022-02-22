import httplib
import json
import click
import socket
from contextlib import closing
from flask import Flask, request, jsonify

app = Flask(__name__)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def do_httptest(ip, port, client_port):
    try:
        conn = httplib.HTTPConnection(ip,
                                      port,
                                      source_address=('', client_port or 37898))
        conn.request(method='GET', url='/')
        resp = conn.getresponse()
        data = json.loads(resp.read())
        print 'data:', data
        return data['client_port']
    except Exception as e:
        raise Exception('ip:[{}], port:[{}], client_port:[{}] err:{}'.format(
            ip, port, client_port, e))


@app.route('/httptest', methods=['GET'])
def httptest():
    ip = str(request.args.get('ip'))
    port = int(request.args.get('port'))
    print 'target:', ip, port
    client_port = find_free_port() or None
    print 'client_port:', client_port
    try:
        client_port_seen_by_server = do_httptest(ip, port, client_port)
        return jsonify({
            'ok': True,
            'same_client_port': client_port == client_port_seen_by_server,
            'client_port_seen_by_server': client_port_seen_by_server,
            'client_port': client_port,
            'server_ip': ip,
            'server_port': port
        })
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e),
            'server_ip': ip,
            'server_port': port
        })


@click.command()
@click.option('--port', default=80)
def main(port):
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
