from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import authenticate, get_user_model

from .models import Contacts

from .serializers import ContactsSerializer

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

    #TODO try except
    name = request.data['name']
    phone = request.data['phone']
    address = request.data['address']

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

    #TODO try except
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