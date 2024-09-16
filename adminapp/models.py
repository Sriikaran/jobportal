from django.db import models

# Create your models here.
class News(models.Model):
    newstext=models.TextField()
    newsdate=models.CharField(max_length=30)
