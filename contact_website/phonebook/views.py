from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets

from .models import Contacts, ContactGroups

from .serializers import ContactsSerializer, ContactGroupsSerializer

SECRET = 'secretword'

# Create your views here.
# class ContactsView(APIView):
#     def

User = get_user_model()
def getuser(token):
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.get(id = payload['id'])

    return user


@api_view(['GET'])
def allContacts(request):

    token = request.COOKIES.get('jwt')
    user = getuser(token)

    contacts = Contacts.objects.filter(user = user)

    serializer = ContactsSerializer(contacts, many = True)
    
    return Response(serializer.data)

@api_view(['GET'])
def contactDetails(request, pk):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    contact = Contacts.objects.get(id = pk)

    if not contact.user == user:
        raise AuthenticationFailed('Unauthenticated')

    serializer = ContactsSerializer(contact)
    
    return Response(serializer.data)


@api_view(['POST'])
def contactUpdate(request, pk):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    contact = Contacts.objects.get(id = pk)

    if not contact.user == user:
        raise AuthenticationFailed('Unauthenticated')

    try:
        name = request.data['name']
    except:
        name = contact.name

    try:
        phone = request.data['phone']
    except:
        phone = contact.phone

    try:
        address = request.data['address']
    except:
        address = contact.address

    data = {
        "name": name,
        "phone": phone,
        "address": address,
        "user" : user.id
    }

    serializer = ContactsSerializer(instance = contact, data = data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)


@api_view(['POST'])
def createContact(request):
    token = request.COOKIES.get('jwt')

    user = getuser(token)

    name = request.data['name']
    phone = request.data['phone']
    address = request.data['address']

    data = {
        "name": name,
        "phone": phone,
        "address": address,
        "user" : user.id
    }

    serializer = ContactsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def contactDelete(request, pk):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    contact = Contacts.objects.get(id = pk)

    if not contact.user == user:
        raise AuthenticationFailed('Unauthenticated')

    contact.delete()

    response = {
        "message" : "success"
    }

    return Response(response)

@api_view(['GET'])
def allGroups(request):

    token = request.COOKIES.get('jwt')
    user = getuser(token)

    contact_groups = ContactGroups.objects.filter(user = user)

    serializer = ContactGroupsSerializer(contact_groups, many = True)
    
    return Response(serializer.data)

@api_view(['GET'])
def groupDetails(request, pk):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    group = ContactGroups.objects.get(id = pk)

    if not group.user == user:
        raise AuthenticationFailed('Unauthenticated')

    serializer = ContactGroupsSerializer(group)
    
    return Response(serializer.data)

@api_view(['POST'])
def createGroup(request):
    token = request.COOKIES.get('jwt')

    user = getuser(token)

    #TODO try except
    new_group = ContactGroups.objects.create(name = request.data['name'], user = user)
    new_group.save()

    for contact in request.data['contacts']:
            contact_obj = Contacts.objects.get(id = contact['id'])
            new_group.contacts.add(contact_obj)

    serializer = ContactGroupsSerializer(new_group)

    return Response(serializer.data)


@api_view(['DELETE'])
def groupDelete(request, pk):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    group = ContactGroups.objects.get(id = pk)

    if not group.user == user:
        raise AuthenticationFailed('Unauthenticated')

    if not group.contacts.exists():
        group.delete()
        message = "success"
    else:
        message = "Error deleting, the group is not empty"

    response = {
        "message" : message
    }

    return Response(response)

@api_view(['POST'])
def adduserToGroup(request, group_key, contact_key):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    group = ContactGroups.objects.get(id = group_key)

    contact = Contacts.objects.get(id = contact_key)

    if not (group.user == user and contact.user == user):
        raise AuthenticationFailed('Unauthenticated')

    if contact in group.contacts.all():
        message = "Contact already exists"
        response = {
        "message" : message
        }

        return Response(response)
    else:
        group.contacts.add(contact)

        serializer = ContactGroupsSerializer(group)

        return Response(serializer.data)

@api_view(['DELETE'])
def removeuserFromGroup(request, group_key, contact_key):
    token = request.COOKIES.get('jwt')
    user = getuser(token)

    group = ContactGroups.objects.get(id = group_key)

    contact = Contacts.objects.get(id = contact_key)

    if not (group.user == user and contact.user == user):
        raise AuthenticationFailed('Unauthenticated')

    if contact in group.contacts.all():
        group.contacts.remove(contact)
        serializer = ContactGroupsSerializer(group)

        return Response(serializer.data)
    else:
        message = "Contact does not exists"
        response = {
        "message" : message
        }

        return Response(response)
        


        