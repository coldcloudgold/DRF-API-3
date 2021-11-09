from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_anonymous_user = models.BooleanField(verbose_name="Анонимный", default=False)
