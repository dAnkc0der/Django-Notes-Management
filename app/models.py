from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shared_with = models.ManyToManyField(User, related_name='shared_notes')

    history = HistoricalRecords()

    def __str__(self):
        return self.title
