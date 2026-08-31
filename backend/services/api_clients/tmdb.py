from .base import BaseApiClient
from ..dtos import MediaItemDTO

class TmdbClient(BaseApiClient):

    BASE_URL = "https://api.themoviedb.org/3"
    def __init__(self, auth_token:str) -> None:
        super().__init__(
            base_url = self.BASE_URL,
            auth_token = auth_token
            )

    def search_movies(self,query:str, page: int = 1) -> list[MediaItemDTO]:
        endpoint = "search/movie"

        params = {
            "query": query,
            "page":page
        }

        data = self._request("GET",endpoint=endpoint, params=params)
        items = data.get("results", [])

        return [MediaItemDTO.from_tmdb_api(item) for item in items]

    def search_series(self,query:str, page:int = 1) -> list[MediaItemDTO]:
        endpoint = "search/tv"

        params = {
            "query":query,
            "page":page
        }

        data = self._request("GET",endpoint=endpoint, params=params)
        items = data.get("results", [])
        return [MediaItemDTO.from_tmdb_api(item) for item in items]

    def get_movie_details(self,tmdb_id:int) -> MediaItemDTO:    
        endpoint = f"movie/{tmdb_id}"

        params = {
            "append_to_response" : "credits"
        }

        movie = self._request("GET", endpoint=endpoint, params=params)
        return MediaItemDTO.from_tmdb_api(movie)

    def get_series_details(self,tmdb_id:int) -> MediaItemDTO:
        endpoint = f"tv/{tmdb_id}" 
        params = {
            "append_to_response" : "credits"
        }

        series = self._request("GET",endpoint=endpoint,params=params)
        return MediaItemDTO.from_tmdb_api(series)
        

        