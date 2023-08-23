from django.db import models

# Create your models here.

class HelloWorld(models.Model):
    text = models.CharField(max_length=255, null=False)
    score = models.FloatField(default=0.0)
    user_ip = models.CharField(max_length=15, default='127.0.0.1')
