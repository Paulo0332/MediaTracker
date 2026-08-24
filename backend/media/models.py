from django.db import models
from django.urls import reverse

# Create your models here.

class MetaTime(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Media(MetaTime):

    class MediaType(models.TextChoices):
        ANIME = "AN", "ANIME"
        MOVIE = "MV", "MOVIE"
        SERIES = "SR", "SERIES"
        BOOK = "BK", "BOOK"
        ALBUM = "AL", "ALBUM"
        GAME = "GM", "GAME"

    title = models.CharField(verbose_name="Title", max_length=255)
    creator = models.CharField(verbose_name="Creator",max_length=255)
    summary = models.TextField(verbose_name="Summary", max_length=1000, blank=True)
    media_type = models.CharField(max_length=2, choices=MediaType.choices, default=MediaType.MOVIE)
    release_date = models.SmallIntegerField(verbose_name="Release Date", null=True, blank=True)
    cover = models.URLField(verbose_name="URL Cover", blank=True,null=True)
    external_id = models.CharField(verbose_name="API Id's", max_length=255,unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("media:media-detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return f"{self.title} - ({self.get_media_type_display()})"   # type: ignore (pylance not recognizing a Django handled function)

   