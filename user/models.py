from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __repr__(self):
        return '<User %s>' % self.username

    def __str__(self):
        return self.username
