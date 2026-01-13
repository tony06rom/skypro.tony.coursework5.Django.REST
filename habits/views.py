from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit, HabitEvent
from .serializers import HabitSerializer, HabitEventSerializer


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
        return Habit.objects.filter(user=user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        habit = self.get_object()
        event = HabitEvent.objects.create(
            habit=habit,
            status=HabitEvent.STATUS_DONE,
        )
        serializer = HabitEventSerializer(event)
        return Response(serializer.data)


class HabitEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return HabitEvent.objects.filter(habit__user=user)
