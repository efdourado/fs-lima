from django.db import models
from django.contrib.auth.models import User

class Mentor(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Mentee(models.Model):
    stages = [
        ('e1', '10 - 1k'),
        ('e2', '1k - 10k'),
        ('e3', '10k - 100k'),
        ('e4', '100k - 1M'),
        ('e5', '1M - 10M'),
        ('e6', '10M - 100M'),
        ('e7', '100M - 1B'),
        ('e8', '1B+'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='mentorship_images/', null=True, blank=True)
    stage = models.CharField(max_length=2, choices=stages)
    mentor = models.ForeignKey(Mentor, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name