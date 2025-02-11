from django.urls import path
from . import  views
app_name = "map"
urlpatterns = [
    path('',  views.Map.as_view(), name='map_view'),
]