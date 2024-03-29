from django.urls import path, include
from .views import TodoViewsSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('todo', TodoViewsSet, basename='todo')
urlpatterns = [
    path('', include(router.urls))
]