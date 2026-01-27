from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from core import settings
from media.models import MetaTime,Media

# Create your models here.

class UserMediaList(MetaTime):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="my_collection")
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="tracked_by")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user","media"], name="user_unique_movie")
        ]

    class Status(models.TextChoices):
        PLAN_TO_START = "PTS","PLAN TO START"
        IN_PROGRESS = "PRG", "IN PROGRESS"
        COMPLETED = "COM", "COMPLETED"
        ON_HOLD = "ONH", "ON HOLD"
        DROPPED = "DRP", "DROPPED"

    def clean(self):
        super().clean()

        if (self.rating is not None or self.review is not None) and self.status in [self.Status.PLAN_TO_START]:
                error_message = "You can't rate or review something you didn't even start!"
                raise ValidationError({
                    "rating": ValidationError(message=error_message, code="invalid_interaction_status"),
                    "review": ValidationError(message=error_message, code="invalid_interaction_status")
                      }
                )

    status = models.CharField(verbose_name="Status",max_length=3, choices=Status.choices, default=Status.PLAN_TO_START)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],blank=True, null=True)
    review = models.TextField(verbose_name="User's Review", max_length=1000,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.media.title} - {self.status}"