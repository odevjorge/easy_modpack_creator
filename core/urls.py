from django.contrib import admin
from django.urls import path, include

import web.urls

urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
]
