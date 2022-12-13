from django.db import models

# Create your models here.

class client(models.Model):
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    docCount = models.IntegerField()
    Role = models.CharField(max_length=15)
