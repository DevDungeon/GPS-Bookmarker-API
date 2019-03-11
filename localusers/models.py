from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField


class LocalUser(AbstractUser):
    premium = BooleanField()
