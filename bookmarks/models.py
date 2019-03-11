from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, DateTimeField, TextField

from localusers.models import LocalUser


class Bookmark(models.Model):
    user = ForeignKey(LocalUser, related_name='bookmarks', on_delete=models.CASCADE)
    lat = TextField()
    lon = TextField()
    alt = TextField()
    timestamp = DateTimeField(auto_now_add=True)

