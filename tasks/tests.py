from django.contrib.auth import login
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
import datetime

from django.urls import reverse

from tasks.views import IndexView
from .models import Tasks


# Create your tests here.
class TestTasks(TestCase):
    def setUp(self):
        print("setup")
        self.user1 = User.objects.create(username="shailesh", password="shailesh")
        self.user2 = User.objects.create(username="testUser", password="password")
        self.task1 = Tasks.objects.create(user=self.user1, TaskName='Test Task',
                                          Description="this is an automated testing", DueDate=datetime.date.today(),
                                          priority=2)

    def tearDown(self):
        print("tearDown")

    def test_user(self):
        print("test user")
        self.assertEqual(self.user1.username, 'shailesh')
        self.assertEqual(self.user1.password, 'shailesh')
        self.assertEqual(self.user2.username, 'testUser')
        self.assertEqual(self.user2.password, 'password')

    def test_createTask(self):
        self.assertEqual(self.task1.user.username, 'shailesh')
        self.assertEqual(self.task1.TaskName, "Test Task")
        self.assertEqual(self.task1.Description, "this is an automated testing")
        self.assertEqual(self.task1.DueDate, datetime.date.today())
        self.assertEqual(self.task1.priority, 2)

    def test_get_absolute_url(self):
        print("testing url")
        print("pk is ", self.task1.pk)
        # self.assertEqual(self.task1.get_absolute_url(), reverse('tasks:detail', kwargs=dict(pk=self.task1.pk)))
        self.assertEqual(self.task1.get_absolute_url(), '/1/')

    def test_object_name(self):
        expected_object_name = f'{self.task1.TaskName}'
        self.assertEqual(str(self.task1), expected_object_name)


# _____________TESTING VIEWS NOW_____________________-

class TaskIndexView(TestCase):
    @classmethod
    def setUpTestData(cls):
        numUsers = 5
        for user_id in range(numUsers):
            User.objects.create(username=f'user{user_id}', password=f'pass{user_id}')
        numTasks = 5
        for task_id in range(1, numTasks):
            Tasks.objects.create(user=User.objects.get(id=task_id % 5), TaskName=f'task{task_id}',
                                 Description=f'task_desc{task_id}',
                                 DueDate=datetime.date.today() + datetime.timedelta(days=task_id), priority=task_id)

    def setUp(self):
        self.factory = RequestFactory()

    def test_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 302)  # redirects to login page.
        login = self.client.login(username='user1', password='pass1')
        response = self.client.get("",follow=True)
        print("error here", response.status_code)
        self.assertEqual(response.status_code, 302)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)  # user is logged in , does not redirects

        # Check we used correct template
        self.assertTemplateUsed(response, 'tasks/homepage.html')
