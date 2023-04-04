from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
   user = models.OneToOneField(to=User,on_delete=models.DO_NOTHING) 
   privatekey = models.CharField(max_length=64)