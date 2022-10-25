from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Film(models.Model):
    name  = models.CharField(max_length=128, unique= True)
    users = models.ManyToManyField(User, related_name='films') # allows you to write user.films.all() instead of Film.objects.all()
