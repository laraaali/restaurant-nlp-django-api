from django.urls import path
from .views import review_list_create

urlpatterns = [
    path("reviews/", review_list_create),
]