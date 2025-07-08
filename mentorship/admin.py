from django.contrib import admin
from .models import Mentee, Mentor, Availability, Meeting, Upload

admin.site.register(Mentee)
admin.site.register(Mentor)
admin.site.register(Availability)
admin.site.register(Meeting)
admin.site.register(Upload)