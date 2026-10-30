from django.contrib import admin
from .models import UploadedFile , UserQuery

admin.site.register(UploadedFile)
admin.site.register(UserQuery)