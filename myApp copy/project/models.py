from django.db import models

# Create your models here.
# models.py

from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.name
