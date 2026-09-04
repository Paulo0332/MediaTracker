from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MediaItemDTO:
    id : int
    title: str
    media_type: str
    provider: str
    release_date: Optional[int]
    overview: Optional[str]
    cover: Optional[str]

    genres: Optional[tuple[str,...]] = None
    creator: Optional[str] = None
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None
    runtime: Optional[int] = None

    @staticmethod
    def extracting_director_movie(raw_payload: dict) -> str | None:
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
    def extracting_creator_series(raw_payload: dict) -> str | None:
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

    @classmethod
    def from_tmdb_api(cls, raw_payload: dict) -> "MediaItemDTO":
        raw_id = raw_payload["id"]

        if "title" in raw_payload:
            raw_title = raw_payload["title"]
            extracted_creator = cls.extracting_director_movie(raw_payload=raw_payload)
            type_media = "MOVIE"
            date_key = "release_date"

            
        elif "name" in raw_payload:
            raw_title = raw_payload["name"]
            extracted_creator = cls.extracting_creator_series(raw_payload=raw_payload)
            type_media = "SERIES"
            date_key = "first_air_date"

        else:
            raw_title = "Unknown"
            extracted_creator = "Unknown"
            type_media = "Unknown"
            date_key = None

        raw_date = raw_payload.get(date_key)
        parsed_year = None
        if raw_date and isinstance(raw_date,str) and len(raw_date)>=4:
            year = raw_date[:4]
            if year.isdigit():
                parsed_year = int(year)

        raw_image_path = raw_payload.get("poster_path")
        complete_path = f"https://image.tmdb.org/t/p/w500{raw_image_path}" if raw_image_path else None
        

        summary = raw_payload.get("overview")
        raw_genres = raw_payload.get("genres")
        parsed_genres = None

        if isinstance(raw_genres,list):
            parsed_genres = tuple(g["name"] for g in raw_genres if isinstance(g,dict) and "name" in g)

        raw_runtime = raw_payload.get("runtime") 
        raw_seasons = raw_payload.get("number_of_seasons")
        raw_episodes = raw_payload.get("number_of_episodes")
    

        return cls(
            id = raw_id,
            title= raw_title,
            release_date = parsed_year,
            cover = complete_path,
            media_type = type_media,
            provider = "tmdb",
            overview = summary,
            genres = parsed_genres,
            runtime = raw_runtime,
            creator = extracted_creator,
            number_of_seasons = raw_seasons,
            number_of_episodes = raw_episodes,
        )   
        
