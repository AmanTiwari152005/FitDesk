from django.db import models
from gym.models import Gym

class Expense(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
