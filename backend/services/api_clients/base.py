import httpx

class ApiClientError(Exception):
    pass

class ApiNetworkError(ApiClientError):
    pass

class ApiTimeoutError(ApiNetworkError):
    pass

class ApiStatusError(ApiClientError):
    pass

class BaseApiClient:
    def __init__(self, base_url: str, auth_token: str, connect_timeout: float = 3.0, read_timeout: float = 8.0) -> None:
        self.base_url = base_url.rstrip("/")

        default_headers = {
            "Authorization":f"Bearer {auth_token}",
            "Accept":"application/json",
            "User-Agent":"MediaTracker/1.0",
        }

        timeout_policy = httpx.Timeout(
            connect= connect_timeout,
            read= read_timeout,
            write= 5.0,
            pool= 5.0,
        )

        self._session = httpx.Client(
            base_url=self.base_url, 
            headers=default_headers, 
            timeout= timeout_policy, 
            follow_redirects=True,
        )

    def _request(self, method:str, endpoint:str, params:dict | None = None, json_data: dict | None = None):
        url = f"/{endpoint.lstrip('/')}"

        try:
            response = self._session.request(method=method,url=url,params=params,json=json_data)

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException as exc:
            raise ApiTimeoutError(f"The API timed out at [{url}]") from exc

        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            raise ApiStatusError(f"The API returned status {code} for [{url}]") from exc

        except httpx.RequestError as exc:
            raise ApiNetworkError(f"Transport network error at [{url}]: {exc}") from exc
            

    def close(self) -> None:
        self._session.close()