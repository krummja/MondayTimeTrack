from __future__ import annotations
from pprint import pprint
from typing import *

if TYPE_CHECKING:
    pass
    
import os
from monday_time_track.monday_sdk_py.client import MondayClientSDK


def get_column_value_service(token: str, item_id: str, column_id: str) -> Any:
    client_id = os.environ['CLIENT_ID']
    monday = MondayClientSDK(token, client_id)
    
    query = (
        '''
        query ($itemId: [Int], $columnId: [String]) {
        items (ids: $itemId) {
            column_values (ids: $columnId) {
            value
            }
        }
        }
        '''
    )

    variables = {
        'itemId': item_id,
        'columnId': column_id,
    }

    response = monday.api(query, **variables)
    pprint(vars(response))


def mutate_column_value_service(
        token: str, 
        board_id: str, 
        item_id: str, 
        column_id: str, 
        value
    ):
    client_id = os.environ['CLIENT_ID']
    monday = MondayClientSDK(token, client_id)
    
    query = (
        '''
        mutation change_column_value ($boardId: Int!, $itemId: Int!, $columnId: String!, $value: JSON!) {
          change_column_value (boardId: $boardId, itemId: $itemId, columnId: $columnId, value: $value) {
            id
          }
        }
        '''
    )
    
    variables = {
        'boardId': board_id,
        'itemId': item_id,
        'columnId': column_id,
        'value': value,
    }
    
    response = monday.api(query, **variables)
    pprint(vars(response))
