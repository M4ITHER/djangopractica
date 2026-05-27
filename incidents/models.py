from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Incident(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved = models.BooleanField(default=False)
    reported_by = models.ForeignKey(    # <- ADD this
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_incidents'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-reported_at'] # Newest first