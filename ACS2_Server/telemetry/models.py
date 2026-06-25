from django.db import models
from django.contrib.auth.models import User

class Stint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_uuid = models.CharField(max_length=100, unique=True)

    game = models.CharField(max_length=50)
    track = models.CharField(max_length=100)
    car = models.CharField(max_length=100, default="unknown")

    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

class TelemetryLap(models.Model):
    stint = models.ForeignKey("Stint", on_delete=models.CASCADE, related_name="laps")

    lap_number = models.IntegerField()

    lap_time = models.FloatField()

    best_lap = models.FloatField(null=True, blank=True)

    driver_name = models.CharField(max_length=100, null=True, blank=True)
    driver_slot = models.IntegerField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)