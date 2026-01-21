from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from user_media.models import UserMediaList
from media.models import Media
# Create your tests here.

class UserMediaTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="apollo",password="wakeupneo547",email="apollo@placeholder.com")
        self.media = Media.objects.create(title="Rocky",creator="Sylvester Stallone",media_type=Media.MediaType.MOVIE)

    def test_create_user_entry(self):
        entry = UserMediaList.objects.create(user=self.user,media=self.media,status=UserMediaList.Status.PLAN_TO_START)

        self.assertEqual(entry.user.username, "apollo")
        self.assertEqual(entry.media.title, "Rocky")

    def test_duplicate_user_email(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(username="test_subject",password="ahahahah",email="apollo@placeholder.com")

    def test_duplicate_user_entry(self):
        UserMediaList.objects.create(user=self.user,media=self.media,status=UserMediaList.Status.PLAN_TO_START)

        with self.assertRaises(IntegrityError):
            UserMediaList.objects.create(user=self.user,media=self.media,status=UserMediaList.Status.COMPLETED)
