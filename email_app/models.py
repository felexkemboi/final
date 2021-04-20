from django.db import models

# Create your models here.
#User model
class User(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=150, unique=True, null=False)
    password1 = models.CharField(max_length=150, null=False)
    password2 = models.CharField(max_length=150, null=False)

#Message model
class Message(models.Model):
    created_at= models.DateTimeField(auto_now_add=True)
    To = models.EmailField(null=False)
    From = models.EmailField(null=False)
    subject = models.CharField(max_length=150, null=False)
    body = models.TextField(null=False)
