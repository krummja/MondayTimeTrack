from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from flask import Request, Response
    
import os
import jwt
import json
from http import HTTPStatus
from flask import make_response, session
from loguru import logger
from jwt.exceptions import *


def authenticate(req: Request) -> Response:
    response = make_response()
    
    try:
        authorization = req.headers.get(
            'Authorization',
            req.args.get('token', '') if req.args else ''
        )

        decoded = jwt.decode(
            authorization,
            os.environ['SIGNING_SECRET'],
            algorithms=['HS256'],
            options={
                'verify_aud': False,
            },
        )
        
        session['account_id'] = decoded.get('accountId')
        session['user_id'] = decoded.get('userId')
        session['short_lived_token'] = decoded.get('shortLivedToken')
        return response
    
    except InvalidTokenError as err:
        logger.debug(err)
        response.data = json.dumps(err.args)
        response.status = HTTPStatus.INTERNAL_SERVER_ERROR
        return response
