from __future__ import annotations
from http.client import HTTPException
from pprint import pprint
from typing import *

if TYPE_CHECKING:
    from flask import Request, Response

import os
import json
from http import HTTPStatus
from flask import make_response, session

from monday_time_track.services.monday_svc import (
    get_column_value_service, 
    mutate_column_value_service,
)

from monday_time_track.services.transform_svc import transform_text_service
from monday_time_track._types import TRANSFORMATION_TYPES, TransformationType

from sorcery import maybe
from loguru import logger


class MondayController:
    
    def execute_action(self, req: Request) -> Response:
        token = session.pop('short_lived_token')

        payload: Dict[str, Any] = maybe(req).json['payload']
        input_fields: Dict[str, Any] = maybe(payload).get('inputFields')

        text_value = get_column_value_service(
            token       = token,
            item_id     = input_fields['itemId'],
            column_id   = input_fields['sourceColumnId']
        )

        if text_value is None:
            response = make_response()
            response.status = HTTPStatus.OK
            return response

        transformed_value = transform_text_service(
            text_value, 
            input_fields['transformationType']
        )

        mutate_column_value_service(
            token,
            int(input_fields['boardId']),
            int(input_fields['itemId']),
            input_fields['targetColumnId'],
            transformed_value,
        )
        
        response = make_response()
        response.status = HTTPStatus.OK
        return response

    def get_remote_list_options(self) -> Response:
        response = make_response()
        
        try:
            response.headers['Content-Type'] = 'application/json'
            response.data = json.dumps(TRANSFORMATION_TYPES)
            response.status = HTTPStatus.OK
            return response
        
        except HTTPException as err:
            response.headers['Content-Type'] = 'application/json'
            response.data = json.dumps(err.args)
            response.status = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
            