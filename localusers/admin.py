from django.contrib import admin

# Register your models here.
from localusers.models import LocalUser

admin.site.register(LocalUser)
