import os
import requests

from flask import Flask
from flask import request
from flask import Response



app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def _proxy(*args, **kwargs):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, os.environ.get("NEW_DOMAIN")),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == "__main__":
    
    app.run(os.environ.get("PORT", 5000))
    
