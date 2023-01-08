from rest_framework import serializers

from .models import Contacts, ContactGroups

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'phone', 'address', 'user']

class ContactGroupsSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer(many=True, read_only = True)

    class Meta:
        ordering = ['id']
        model = ContactGroups
        fields = ['id', 'name', 'user', 'contacts']
        extra_kwargs = {
            'contacts' : {'required': False}
        }