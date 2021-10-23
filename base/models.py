from datetime import timezone, datetime, date
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#The Task model, to collect users todo list inputs
class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    start = models.DateTimeField(default= datetime.now, blank=True)
    end = models.DateTimeField(default= datetime.now, blank=True)
    file = models.FileField(upload_to='documents/', null=True)
    # image = models.ImageField(upload_to='images/', null=True)





    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'
