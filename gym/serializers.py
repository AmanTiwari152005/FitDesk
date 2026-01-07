from rest_framework import serializers
from .models import Gym

class GymSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Gym
        fields = [
            "gym_name",
            "address",
            "opening_time",
            "closing_time",
            "monthly_fee",
            "quarterly_fee",
            "yearly_fee",
            "owner_name"
        ]
