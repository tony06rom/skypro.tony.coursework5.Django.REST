from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitEventViewSet, HabitViewSet

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habit")
router.register("events", HabitEventViewSet, basename="event")

urlpatterns = [
    path("", include(router.urls)),
]
