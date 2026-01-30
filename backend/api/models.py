from django.db import models
from django.utils import timezone

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
