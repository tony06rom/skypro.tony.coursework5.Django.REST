from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Habit, HabitEvent
from .serializers import HabitEventSerializer, HabitSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Habit):
            if request.method in permissions.SAFE_METHODS:
                return obj.is_public or obj.user == request.user
            return obj.user == request.user
        return False


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = Habit.objects.filter(user=user)
        is_pleasant = self.request.query_params.get("is_pleasant")
        if is_pleasant is not None:
            qs = qs.filter(is_pleasant=is_pleasant.lower() == "true")
        return qs

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        habit = self.get_object()
        event = HabitEvent.objects.create(habit=habit, status=HabitEvent.STATUS_DONE)
        serializer = HabitEventSerializer(event)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        habit = self.get_object()
        total_done = habit.events.filter(status=HabitEvent.STATUS_DONE).count()
        total_missed = habit.events.filter(status=HabitEvent.STATUS_MISSED).count()
        return Response(
            {
                "habit_id": habit.id,
                "total_done": total_done,
                "total_missed": total_missed,
            }
        )


class HabitEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HabitEvent.objects.filter(habit__user=self.request.user)
