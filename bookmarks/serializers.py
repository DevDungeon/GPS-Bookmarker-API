from rest_framework import serializers
from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'lat', 'lon', 'alt', 'timestamp', 'url')
