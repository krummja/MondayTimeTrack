from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from flask import Flask
    

import os
import re
import shutil
from threading import Timer

from monday_time_track import create_app


def open_tunnel(port: int, subdomain: Optional[str] = None) -> int:
    if not shutil.which('lt'):
        os.system('npm install -g localtunnel')
    command = f'lt -p {port}'
    if subdomain:
        subdomain = subdomain.strip()
        subdomain = subdomain.replace('.', '-')
        subdomain = subdomain.replace(' ', '-')
        if re.match(r"^[\w-]+$", subdomain):
            command += f' -s {subdomain.lower()}'
    output = os.system(command)
    return output


def start_localtunnel(port: int, subdomain: Optional[str] = None) -> None:
    address = open_tunnel(port, subdomain)
    print(address)


def with_localtunnel(app: Flask, subdomain: Optional[str] = None) -> None:
    _run = app.run

    def run(*args, **kwargs):
        _port = kwargs.get('port', 8080)
        _thread = Timer(1, start_localtunnel, args=(_port, subdomain,))
        _thread.daemon = True
        _thread.start()
        _run(*args, **kwargs)

    app.run = run


if __name__ == '__main__':
    server_app = create_app()
    with_localtunnel(server_app, 'monday-time-track')
    server_app.run(host="localhost", port=8080, debug=True)
else:
    server_app = create_app()
