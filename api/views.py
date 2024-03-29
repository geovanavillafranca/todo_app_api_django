from django.shortcuts import render
from .serializers import TodoSerializer
from .models import Todo
from rest_framework import viewsets
# Create your views here.


class TodoViewsSet(viewsets.ModelViewSet):
    """.
    A simple viewset for viewing and editing Todo instances
    """
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    