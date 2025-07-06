from django.contrib import admin
from .models import Mentee, Mentor, Availability

admin.site.register(Mentee)
admin.site.register(Mentor)
admin.site.register(Availability)