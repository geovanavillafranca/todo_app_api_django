from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..models import Todo
from rest_framework import status
from ..views import TodoViewsSet
import json
# Create your tests here.

class TodoModelTestCase(TestCase):
    pass

class TodoViewSetTestCase(TestCase):
    def setUp(self):
        self.url = '/api/todo/'
        self.factory = APIRequestFactory()
        self.todo = {'name':'Task 1', 'isCompleted': True}
    
    def test_empty_todo_list_200_response(self):
        """
        Test return empty Todo list, without creating a task
        """
        view = TodoViewsSet.as_view({'get': 'list'})
        request = self.factory.get(self.url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_return_todo_list_200_response(self):
        """
        Test return Todo list
        """
        view = TodoViewsSet.as_view({'get': 'list', 'post': 'create'})

        request1 = self.factory.post(self.url, data=self.todo)
        response1 = view(request1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        request2 = self.factory.post(self.url, data={'name': 'Task 2'})
        response2 = view(request2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        request = self.factory.get(self.url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_a_task_201_response(self):
        """
        Test create a task
        """
        
        view = TodoViewsSet.as_view({'post':'create'})
        request = self.factory.post(self.url, data=self.todo)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().name, 'Task 1')

    def test_create_an_empty_task_400_response(self):
        """
        Test creating a task empty
        """

        view = TodoViewsSet.as_view({'post': 'create'})
        request = self.factory.post(self.url, data={})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_existing_id_200_response(self):
        """
        Test filter an existing task by ID
        """

        view = TodoViewsSet.as_view({'post':'create', 'get':'retrieve'})
        request1 = self.factory.post(self.url, data=self.todo)
        response1 = view(request1)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        id = response1.data['id']
        request = self.factory.get(f"{self.url}{id}")
        response = view(request, **{'pk':id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], response1.data['name'])

    def test_filter_by_unexisting_id_404_response(self):
        """
        Test filter by unexisting id
        """
        view = TodoViewsSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f"{self.url}2")
        response = view(request, **{'pk':2})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_name_200_response(self):
        """
        Test updating a task 
        """
        view = TodoViewsSet.as_view({'put': 'update', 'post': 'create'})
        request = self.factory.post(self.url, data=self.todo)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data['id']
        request = self.factory.put(f"{self.url}{id}", data={"name":"Update task name"})
        response = view(request, **{'pk':id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Update task name")

    def test_update_task_without_data_400_response(self):
        """
        Test updating a task without data
        """
        view = TodoViewsSet.as_view({'put': 'update', 'post': 'create'})
        request = self.factory.post(self.url, data=self.todo)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data['id']
        request = self.factory.put(f"{self.url}{id}", data={})
        response = view(request, **{'pk':id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_with_unexisting_task_404_response(self):
        """
        Test updating a task that doesn't exist
        """
        
        view = TodoViewsSet.as_view({'put': 'update'})

        id = 2
        request = self.factory.put(f"{self.url}{id}", data={"name":"Update task name"})
        response = view(request, **{'pk':id})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_200_response(self):
        """
        Test deleting a task
        """
        view = TodoViewsSet.as_view({'delete': 'destroy', 'post': 'create'})
        request = self.factory.post(self.url, data=self.todo)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data['id']
        request = self.factory.delete(f"{self.url}{id}")
        response = view(request, **{'pk': id})
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_unexisting_task_404_response(self):
        """
        Test deleting a task that doesn't exist
        """
        view = TodoViewsSet.as_view({'delete': 'destroy'})
        id = 2
        request = self.factory.delete(f"{self.url}{id}")
        response = view(request, **{'pk': id})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

