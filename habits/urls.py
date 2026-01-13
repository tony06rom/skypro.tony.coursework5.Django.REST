from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, HabitEventViewSet

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habit")
router.register("events", HabitEventViewSet, basename="event")

urlpatterns = [
    path("", include(router.urls)),
]
