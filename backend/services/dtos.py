from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MediaItemDTO:
    id : int
    title: str
    media_type: str
    provider: str
    release_year: Optional[int]
    overview: Optional[str]
    cover: Optional[str]

    genres: Optional[tuple[str,...]] = None
    creator: Optional[str] = None
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None
    runtime: Optional[int] = None

   
    @staticmethod
    def extract_movie_directors(raw_payload: dict) -> str | None:
        raw_credits = raw_payload.get("credits")
        if not isinstance(raw_credits,dict):
            return None
        raw_crew = raw_credits.get("crew")
        if not isinstance(raw_crew,list):
            return None
        extracted_creators = []
        for member in raw_crew:
            if isinstance(member,dict) and member.get("job") == "Director":
                creator = member.get("name")
                if creator:
                    extracted_creators.append(creator)
        return ", ".join(extracted_creators) if extracted_creators else None

    @staticmethod
    def extract_series_creators(raw_payload: dict) -> str | None:
        raw_created_by = raw_payload.get("created_by")
        if not isinstance(raw_created_by, list):
            return None
        extracted_creators = []
        for member in raw_created_by:
            if isinstance(member,dict):
                creator = member.get("name")
                if creator:
                    extracted_creators.append(creator)
        return ", ".join(extracted_creators) if extracted_creators else None

    @staticmethod
    def parse_release_year(raw_date: str | None) -> int | None:
        parsed_year = None
        
        if isinstance(raw_date,str) and len(raw_date)>=4:
            year = raw_date[:4]
            if year.isdigit():
                parsed_year = int(year)

        return parsed_year

    @staticmethod
    def build_poster_url(raw_payload: dict) -> str | None:
        raw_image_path = raw_payload.get("poster_path")
        complete_path = f"https://image.tmdb.org/t/p/w500{raw_image_path}" if raw_image_path else None

        return complete_path

    @staticmethod
    def parse_genres(raw_payload:dict) -> tuple[str,...] | None:
        raw_genres = raw_payload.get("genres")
        parsed_genres = None

        if isinstance(raw_genres,list):
            parsed_genres = tuple(g["name"] for g in raw_genres if isinstance(g,dict) and "name" in g)

        return parsed_genres

    @classmethod
    def from_tmdb_movie(cls, raw_payload: dict) -> "MediaItemDTO":
        raw_id = raw_payload["id"]
        raw_title = raw_payload["title"]
        extracted_creator = cls.extract_movie_directors(raw_payload=raw_payload)
        raw_date = raw_payload.get("release_date")
        parsed_year = cls.parse_release_year(raw_date=raw_date)
        complete_path = cls.build_poster_url(raw_payload=raw_payload)
        summary = raw_payload.get("overview")
        parsed_genres = cls.parse_genres(raw_payload=raw_payload)

        raw_runtime = raw_payload.get("runtime")

        return cls(
            id = raw_id,
            title = raw_title,
            media_type = "MOVIE",
            provider = "tmdb",
            release_year = parsed_year,
            overview = summary,
            cover = complete_path,
            genres = parsed_genres,
            runtime = raw_runtime,
            creator = extracted_creator,
        )

    @classmethod
    def from_tmdb_series(cls, raw_payload: dict) -> "MediaItemDTO":
        raw_id = raw_payload["id"]
        raw_title = raw_payload["name"]
        extracted_creator = cls.extract_series_creators(raw_payload=raw_payload)
        raw_date = raw_payload.get("first_air_date")
        parsed_year = cls.parse_release_year(raw_date=raw_date)
        complete_path = cls.build_poster_url(raw_payload=raw_payload)
        summary = raw_payload.get("overview")
        parsed_genres = cls.parse_genres(raw_payload=raw_payload)

        raw_seasons = raw_payload.get("number_of_seasons")
        raw_episodes =raw_payload.get("number_of_episodes")

        return cls(
            id = raw_id,
            title = raw_title,
            media_type = "SERIES",
            provider = "tmdb",
            release_year = parsed_year,
            overview = summary,
            cover = complete_path,
            genres = parsed_genres,
            creator = extracted_creator,
            number_of_seasons = raw_seasons,
            number_of_episodes = raw_episodes
        )

