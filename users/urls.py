from django.urls import path
from .views import CreateAnonymousUser

urlpatterns = [
    path("anonymous_users/", CreateAnonymousUser.as_view()),
]
