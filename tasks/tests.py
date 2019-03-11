from django.conf.urls import url
from django.contrib.auth import login
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
import datetime

from django.urls import reverse, reverse_lazy

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

        response = self.client.get("", follow=True)
        print("error here", response.status_code)
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)  # user is logged in , does not redirects

        # Check we used correct template
        self.assertTemplateUsed(response, 'tasks/homepage.html')
        self.client.logout()


# __________CHECKING VIEW PROTECTION_____________


class EditTaskByUserViewTest(TestCase):
    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(username='testuser1', password='testuser1')
        self.test_user2 = User.objects.create_user(username='testuser2', password='testuser2')

        self.test_user1.save()
        self.test_user2.save()

        # Create a book
        self.test_task1 = Tasks.objects.create(user=User.objects.get(id=1), TaskName='user1\'s task',
                                               Description='abcd',
                                               DueDate=datetime.date.today() + datetime.timedelta(days=1), priority=1)
        self.test_task2 = Tasks.objects.create(user=User.objects.get(id=2), TaskName='user2\'s task',
                                               Description='abcd',
                                               DueDate=datetime.date.today() + datetime.timedelta(days=2), priority=1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('')
        self.assertRedirects(response, '/login')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1')
        response = self.client.get("", follow=True)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'tasks/todolist40.html')

        # checking user1 can view, edit or delete task of user2
        response = self.client.get(reverse('tasks:detail', kwargs=dict(pk=self.test_task2.pk)))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('tasks:update_task', kwargs=dict(pk=self.test_task2.pk)))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('tasks:delete_task', kwargs=dict(pk=self.test_task2.pk)))
        self.assertEqual(response.status_code, 404)
        self.client.logout()
