from __future__ import annotations
from pprint import pprint
from typing import *

if TYPE_CHECKING:
    from flask import Request, Response

import os
from dotenv import load_dotenv
from flask import (
    Flask, 
    request,
    session,
)
from loguru import logger

from monday_time_track.controllers.monday_controller import MondayController
from monday_time_track.middlewares import authentication
from monday_time_track.logging_utils import configure_external_log


load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ['SIGNING_SECRET']
    
    configure_external_log()
    
    controller = MondayController()
    
    @app.route('/health', methods=['GET'])
    def health() -> str:
        logger.info('Server up!')
        return 'Server up!'
    
    @app.route('/execute_action', methods=['POST'])
    def execute_action():
        authentication.authenticate(request)
        return ''
    
    @app.route('/get_remote_list_options', methods=['POST'])
    def field_definition() -> Response:
        authentication.authenticate(request)
        return controller.get_remote_list_options()
    
    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        _req: Request = request
        logger.info(vars(_req))
        return ''
    
    @app.route('/unsubscribe', methods=['POST'])
    def unsubscribe():
        _req: Request = request
        logger.info(vars(_req))
        return ''
    
    @app.route('/update_time_tracking', methods=['POST'])
    def update_time_tracking():
        _req: Request = request
        logger.info(vars(_req))
        return ''
    
    return app
