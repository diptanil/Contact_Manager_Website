from django.urls import path
from .views import allContacts, createContact, contactDetails, contactUpdate, contactDelete

urlpatterns = [
    path('', allContacts, name='all-contacts'),
    path('detail/<str:pk>/', contactDetails, name='contact-details'),
    path('create/', createContact, name='create-contacts'),
    path('update/<str:pk>/', contactUpdate, name='contact-update'),
    path('delete/<str:pk>/', contactDelete, name='contact-delete'),
]
