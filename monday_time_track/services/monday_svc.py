from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from requests import Response
    
import os
from monday_time_track.monday_sdk.client import MondayClientSDK
from sorcery import maybe


def get_column_value_service(token: str, item_id: str, column_id: str) -> Any:
    client_id = os.environ['CLIENT_ID']
    
    monday = MondayClientSDK(
        client_id=client_id, 
        api_token=token,
    )
    
    query = (
        """
        query ($itemId: [Int], $columnId: [String]) {
          items (ids: $itemId) {
            column_values (ids: $columnId) {
              value
            }
          }
        }
        """
    )
    
    variables = {
        'itemId': item_id,
        'columnId': column_id,
    }

    response: Response = maybe(monday).api(query, **variables)

    data = response.json()['data']
    item = data['items'][0]
    column_value = item['column_values'][0]['value']
    return column_value

def mutate_column_value_service(
        token: str, 
        board_id: int, 
        item_id: int, 
        column_id: str, 
        value: str,
    ):
    client_id = os.environ['CLIENT_ID']
    monday = MondayClientSDK(
        client_id=client_id, 
        api_token=token,
    )
    
    query = (
        """
        mutation change_column_value ($boardId: Int!, $itemId: Int!, $columnId: String!, $value: JSON!) {
          change_column_value (board_id: $boardId, item_id: $itemId, column_id: $columnId, value: $value) {
            id
          }
        }
        """
    )
    
    variables = {
        'boardId': board_id,
        'itemId': item_id,
        'columnId': column_id,
        'value': value,
    }
    
    response: Response = maybe(monday).api(query, **variables)
    return response
