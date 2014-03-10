from django.db import models
from authtools.models import AbstractEmailUser


class User(AbstractEmailUser):
    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser
