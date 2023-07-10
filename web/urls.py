from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', config_view, name="config_view"),
    re_path(r'^(?P<version>\d{1,2}(?:\.\d{1,2}){2})/(?P<modloader>any|forge|cauldron|liteloader|fabric|quilt)/$',
            search_mods_view, name="search"),

]
