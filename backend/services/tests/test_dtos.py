from services.dtos import MediaItemDTO 
from django.test import SimpleTestCase

class TestMediaDTOParsing(SimpleTestCase):

    def test_movie_search_payload(self):
        payload = {
            "id": 603,
            "title": "The Matrix",
            "release_date": "1999-03-30",
            "poster_path": "/dXNAPwY7VrqMAo51EKhhCJfaGb5.jpg",
            "overview": "Set in the 22nd century...",
        }

        dto = MediaItemDTO.from_tmdb_api(payload)

        self.assertEqual(dto.id, 603)
        self.assertEqual(dto.title, "The Matrix")
        self.assertEqual(dto.media_type,"MOVIE")
        self.assertEqual(dto.provider, "tmdb")
        self.assertEqual(dto.release_date, 1999)
        self.assertEqual(dto.overview, "Set in the 22nd century...")
        self.assertEqual(dto.cover, "https://image.tmdb.org/t/p/w500/dXNAPwY7VrqMAo51EKhhCJfaGb5.jpg")

    def test_series_search_payload(self):
        payload = {
            "id": 1399,
            "name": "Game of Thrones",
            "first_air_date": "2011-04-17",
            "poster_path": "/u3bZgnGQ9T01sWNhyveQz0wH0Hl.jpg",
            "overview": "Seven noble families fight...",
        }

        dto = MediaItemDTO.from_tmdb_api(payload)

        self.assertEqual(dto.title, "Game of Thrones")
        self.assertEqual(dto.media_type, "SERIES")
        self.assertEqual(dto.release_date, 2011)

    def test_movie_details_credits_genres(self):
        payload = {
            "id": 603,
            "title": "The Matrix",
            "release_date": "1999-03-30",
            "runtime": 136,
            "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Science Fiction"}],
            "credits": {
                "crew": [
                    {"job": "Director", "name": "Lilly Wachowski"},
                    {"job": "Director", "name": "Lana Wachowski"},
                    {"job": "Producer", "name": "Joel Silver"}, # Should be ignored
                ]
            },
        }

        dto = MediaItemDTO.from_tmdb_api(payload)

        self.assertEqual(dto.creator,"Lilly Wachowski, Lana Wachowski")
        self.assertEqual(dto.genres,("Action","Science Fiction"))
        self.assertEqual(dto.runtime, 136)

    def test_series_details_created_by(self):
        payload = {
            "id": 1399,
            "name": "Game of Thrones",
            "first_air_date": "2011-04-17",
            "number_of_seasons": 8,
            "number_of_episodes": 73,
            "created_by": [
                {"name": "David Benioff"},
                {"name": "D.B. Weiss"},
            ],
        }

        dto = MediaItemDTO.from_tmdb_api(payload)

        self.assertEqual(dto.creator,"David Benioff, D.B. Weiss")
        self.assertEqual(dto.number_of_seasons, 8)
        self.assertEqual(dto.number_of_episodes, 73)

    def test_edge_case_date_parsing(self):
        bad_dates = [None, "", "TBD", "N/A", "12"]

        for bad_date in bad_dates:
            payload = {
                "id": 10,
                "name": "Unreleased Indie Movie",
                "release_date": bad_date
            }

            dto = MediaItemDTO.from_tmdb_api(payload)

            self.assertIsNone(dto.release_date, f"Expected None for date:{bad_date}")

    def test_edge_case_missing_cover_and_crew(self):
        payload = {
            "id": 11,
            "name": "Minimal Movie",
            "poster_path": None,
            "credits":{
                "crew": [
                    {"job": "Grip", "name": "John Doe"}
                ]
            }
        }

        dto = MediaItemDTO.from_tmdb_api(payload)

        self.assertIsNone(dto.cover)
        self.assertIsNone(dto.creator)
        