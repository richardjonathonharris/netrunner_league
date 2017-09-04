from django.contrib import admin
from .models import User, Records, Event

admin.site.register(User)
admin.site.register(Records)
admin.site.register(Event)

# Register your models here.
