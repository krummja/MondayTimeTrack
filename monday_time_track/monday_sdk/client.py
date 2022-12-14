from __future__ import annotations
from typing import *
from types import TracebackType

if TYPE_CHECKING:
    from requests import Request, Response

import os
import requests
from requests.auth import AuthBase
from requests.adapters import HTTPAdapter
from requests_toolbelt import sessions

from dotenv import load_dotenv


load_dotenv()


MONDAY_PROTOCOL = os.environ.get('MONDAY_PROTOCOL', 'https')
MONDAY_DOMAIN = os.environ.get('MONDAY_DOMAIN', 'monday.com')
MONDAY_API_URL = f'{MONDAY_PROTOCOL}://api.{MONDAY_DOMAIN}/v2'
MONDAY_OAUTH_URL = f'{MONDAY_PROTOCOL}://auth.{MONDAY_DOMAIN}/oauth2/authorize'
MONDAY_OAUTH_TOKEN_URL = f'{MONDAY_PROTOCOL}://auth.{MONDAY_DOMAIN}/oauth2/token'


class MondayAuth(AuthBase):
    
    def __init__(self, access_token: str) -> None:
        self._token = access_token
        
    def __call__(self, request: Request) -> Request:
        request.headers['Content-Type'] = 'application/json'
        request.headers['Authorization'] = self._token
        return request
    
    
class MondayContext:
    
    def __init__(self, api_token: str) -> None:
        self._base = MONDAY_API_URL
        self._base_ctx = sessions.BaseUrlSession(base_url=self._base)
        self._base_ctx.auth = MondayAuth(api_token)
        self._base_ctx.mount(prefix=self._base, adapter=HTTPAdapter())
        
    def __enter__(self) -> requests.Session:
        return self._base_ctx
    
    def __exit__(
            self,
            exc_type: Type[BaseException],
            exc_val: BaseException,
            exc_tb: TracebackType
        ) -> bool:
        self._base_ctx.close()
        return False


class MondayClientSDK:
    
    def __init__(self, *, client_id: str, api_token: str) -> None:
        self._client_id = client_id
        self._api_token = api_token
    
    def api(self, query, **options):
        params = { 'query': query, 'variables': options }
        token = options.get('api_token', self._api_token)

        if token:
            result = self.execute(params, token)
            return result
            
    def execute(
            self,
            data: Dict[str, Any],
            token: str,
            **options
        ) -> Response | None:
        url = options.get('url', MONDAY_API_URL)
        path = options.get('path', '')
        full_url = url + path
        
        with MondayContext(token) as ctx:
            _res: Response = ctx.request(
                url=full_url,
                method=options.get('method', 'POST'),
                json=data,
            )

            return _res
