from django.db import models
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User
# Create your models here.


class Tasks(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    TaskName = models.CharField(max_length = 100)
    Description = models.CharField(max_length = 400)
    DueDate = models.DateField(help_text="YY-MM-DD")
    priority = models.IntegerField()

    def __str__(self):
        return self.TaskName
    
    def get_absolute_url(self):
        return reverse('tasks:detail',kwargs={'pk':self.pk})
