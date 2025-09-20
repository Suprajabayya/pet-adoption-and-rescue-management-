from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
    )

    name = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=50, default='Dog')
    color = models.CharField(max_length=50, blank=True)
    age = models.CharField(max_length=50, blank=True)
    wound = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_pets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species} ({self.status}) - {self.name or 'Unknown'}"
