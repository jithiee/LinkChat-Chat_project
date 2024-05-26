from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Message(models.Model):
    from_who = models.ForeignKey(User, related_name='from_who', on_delete=models.PROTECT , default=None)
    to_who = models.ForeignKey(User, related_name='to_who', on_delete=models.PROTECT , default=None)
    message = models.TextField()
    date = models.DateField( auto_now=False, auto_now_add=False  ,null= True )
    time = models.TimeField( auto_now=False, auto_now_add=False   , null=True)
    has_been_seen = models.BooleanField(null=True , default=False)

class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT , default=None)
    channel_name = models.TextField()