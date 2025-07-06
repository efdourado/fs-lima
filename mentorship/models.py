from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta

import secrets

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
    token = models.CharField(max_length=16, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token: 
            self.token = self.generate_unique_token()
            super().save(*args, **kwargs)

    def generate_unique_token(self):
        while True:
            token = secrets.token_urlsafe(8)  
            if not Mentee.objects.filter(token=token).exists():
                return token

    def __str__(self):
        return self.name

class Availability(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=50)
    
class Meeting(models.Model):
    tag_choices = (
        ('Ma', 'Management'),
        ('M', 'Marketing'),
        ('HR', 'Human Resources'),
        ('T', 'Taxes')
    )

    date = models.ForeignKey(Availability, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=tag_choices)
    description = models.TextField()