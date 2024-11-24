# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from core import settings  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),  # add this
    path("", include("app.urls"))  # add this
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)