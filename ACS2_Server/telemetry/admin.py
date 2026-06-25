
# Register your models here.
from django.contrib import admin
from .models import Stint, TelemetryLap

admin.site.register(Stint)
admin.site.register(TelemetryLap)