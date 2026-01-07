from django.db import models
from gym.models import Gym


class Member(models.Model):
    PACKAGE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]

    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name="members"
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    package = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES
    )

    join_date = models.DateField()
    expiry_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.package})"

class MemberRenewal(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="renewals")

    package = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.IntegerField()

    renewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} - {self.package}"