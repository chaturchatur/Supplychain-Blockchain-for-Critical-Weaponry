from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Indent(models.Model):
    address = models.CharField(max_length=40)
    owner = models.ForeignKey(to=User,on_delete=models.DO_NOTHING,null=True)

class Part(models.Model):
    part_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
