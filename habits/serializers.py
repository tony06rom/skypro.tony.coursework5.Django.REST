from rest_framework import serializers
from .models import Habit, HabitEvent


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = [
            "id",
            "name",
            "description",
            "period_type",
            "frequency",
            "time",
            "is_pleasant",
            "is_public",
            "created_at",
            "events",
        ]
        read_only_fields = ["id", "created_at", "events"]

    def validate_frequency(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("Частота должна быть не меньше 1")
        if value > 10:
            raise serializers.ValidationError("Слишком большая частота")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return Habit.objects.create(user=user, **validated_data)


class HabitEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEvent
        fields = ["id", "habit", "status", "performed_at"]
        read_only_fields = ["performed_at"]
