from rest_framework import serializers

from .models import Contacts, ContactGroups

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'phone', 'address', 'user']