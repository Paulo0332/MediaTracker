from media.models import Media
from django.db import transaction
from services.dtos import MediaItemDTO as dto

class MediaIngestionService:

    CATEGORY_MAPPING = {
        "ANIME":Media.MediaType.ANIME,
        "MOVIE":Media.MediaType.MOVIE,
        "SERIES":Media.MediaType.SERIES,
        "BOOK":Media.MediaType.BOOK,
        "ALBUM":Media.MediaType.ALBUM,
        "GAME":Media.MediaType.GAME,
    }

    @classmethod
    @transaction.atomic
    def ingest_media(cls,dto: dto) -> "Media":
        safe_title = dto.title[:255]
        safe_creator = (dto.creator or "Unknown")[:255]
        safe_overview = (dto.overview or "")[:1000]
        treated_media_type = cls.CATEGORY_MAPPING.get(dto.media_type,Media.MediaType.MOVIE)
        external_id = f"{dto.provider}-{dto.id}"

        media, _ = Media.objects.update_or_create(
            external_id = external_id,
            defaults={
                "title":safe_title,
                "creator":safe_creator,
                "summary":safe_overview,
                "media_type":treated_media_type,
                "release_date":dto.release_date,
                "cover":dto.cover
            }
        )

        return media