from rest_framework import serializers

from .models import Habit, HabitEvent


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "name",
            "description",
            "place",
            "time",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "events"]

    def validate_frequency(self, value: int) -> int:
        if value < 1:
            raise serializers.ValidationError("Частота должна быть не меньше 1")
        if value > 10:
            raise serializers.ValidationError("Слишком большая частота")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        is_pleasant = data.get("is_pleasant", False)
        related_habit = data.get("related_habit")
        reward = data.get("reward")
        execution_time = data.get("execution_time")
        periodicity = data.get("periodicity")
        if related_habit and reward:
            raise serializers.ValidationError("Нельзя одновременно выбирать связанную привычку и вознаграждение.")
        if execution_time and execution_time > 120:
            raise serializers.ValidationError("Время на выполнение не может быть больше 120 секунд.")
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("В связанные привычки могут попадать только приятные привычки.")
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения " "или связанной привычки."
            )
        if periodicity and periodicity > 7:
            raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
        return data


class HabitEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitEvent
        fields = ["id", "habit", "status", "performed_at"]
        read_only_fields = ["performed_at"]
