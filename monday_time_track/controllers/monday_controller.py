from __future__ import annotations
from http.client import HTTPException
from typing import *

if TYPE_CHECKING:
    from flask import Response

import json
from http import HTTPStatus
from flask import make_response

from monday_time_track.services.monday_svc import (
    get_column_value_service, 
    mutate_column_value_service,
)

from monday_time_track.services.transform_svc import transform_text_service
from monday_time_track._types import TRANSFORMATION_TYPES, TransformationType

from loguru import logger


class TextTransformPayload(TypedDict):
    board_id: str
    item_id: str
    source_column_id: str
    target_column_id: str
    transformation_type: TransformationType


class MondayController:
    
    def execute_action(self, token, payload: TextTransformPayload) -> Response:
        text_value = get_column_value_service(
            token       = token,
            item_id     = payload['item_id'],
            column_id   = payload['source_column_id']
        )
        
        if text_value is None:
            response = make_response()
            response.status = HTTPStatus.OK
            return response
        
        transformed_value = transform_text_service(
            text_value, 
            payload['transformation_type']
        )
        
        mutate_column_value_service(
            token,
            payload['board_id'],
            payload['item_id'],
            payload['target_column_id'],
            transformed_value,
        )
        
        response = make_response()
        response.status = HTTPStatus.OK
        return response

    def get_remote_list_options(self) -> Response:
        response = make_response()
        
        try:
            response.status = HTTPStatus.OK
            response.data = json.dumps(TRANSFORMATION_TYPES)
            logger.debug(response.data)
            return response
        
        except HTTPException as err:
            logger.debug(err)
            response.data = json.dumps(err.args)
            response.status = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
            