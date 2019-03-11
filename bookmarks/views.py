from django.http import HttpRequest
from django.views import View
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class IsPremiumUser(permissions.BasePermission):
    message = "Only Premium users may access this resource."

    def has_permission(self, request: HttpRequest, view: View):
        # return request.user.has_perm('appname.permname')  # Django ACL Perms
        return request.user.premium

    def has_object_permission(self, request: HttpRequest, view: View, obj):
        # See if obj belongs to user?
        return request.user.premium


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# curl -v --cookie "sessionid=e0rje2u3h1uc1ga61ax5fqom9ra29lhq" http://127.0.0.1:8000/api/bookmarks.json
class BookmarksViewSet(DestroyModelMixin,
                       RetrieveModelMixin,
                       ListModelMixin,
                       GenericViewSet):
    queryset = Bookmark.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsPremiumUser)
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request_copy = request.POST.copy()
        request_copy['user'] = str(request.user.id)
        serializer = self.get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
