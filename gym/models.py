from django.db import models
from django.contrib.auth.models import User

class Gym(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=100)
    monthly_fee = models.IntegerField(default=0)
    quarterly_fee = models.IntegerField(default=0)
    yearly_fee = models.IntegerField(default=0)
    address = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gym_name
