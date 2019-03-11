"""GpsbookmarkerAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.urls import include
from rest_framework import routers, serializers, viewsets
import bookmarks.views
import localusers.views
from localusers.models import LocalUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # When using this, it only shows the primary key ID not the url
    #bookmarks = serializers.PrimaryKeyRelatedField(many=True, queryset=Bookmark.objects.all())

    class Meta:
        model = LocalUser
        fields = ('url', 'username', 'email', 'is_staff', 'bookmarks', 'is_superuser', 'premium')


class GroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'url', 'name', 'codename')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')


class UserViewSet(viewsets.ModelViewSet):
    queryset = LocalUser.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = GroupPermissionSerializer














router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'bookmarks', bookmarks.views.BookmarksViewSet)
router.register(r'permissions', GroupPermissionViewSet)











urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls')),  # For web browsable API

    url(r'^api/login/', localusers.views.api_login),
    url(r'^api/logout/', localusers.views.api_logout),

    url(r'^api/', include(router.urls)),

]
