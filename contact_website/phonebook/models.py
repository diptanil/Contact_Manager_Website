from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Contacts(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ContactGroups(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contacts)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name