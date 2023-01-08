from django.urls import path
from .views import allContacts, createContact, contactDetails, contactUpdate, contactDelete
from .views import allGroups, createGroup, groupDetails, groupDelete, adduserToGroup, removeuserFromGroup

urlpatterns = [
    path('', allContacts, name='all-contacts'),
    path('detail/<str:pk>/', contactDetails, name='contact-details'),
    path('create/', createContact, name='create-contacts'),
    path('update/<str:pk>/', contactUpdate, name='contact-update'),
    path('delete/<str:pk>/', contactDelete, name='contact-delete'),

    path('groups/', allGroups, name='all-groups'),
    path('group/<str:pk>/', groupDetails, name='group-details'),
    path('create-group/', createGroup, name='create-group'),
    path('delete-group/<str:pk>/', groupDelete, name='group-delete'),
    path('add-contact/<str:group_key>/<str:contact_key>/', adduserToGroup, name='group-add'),
    path('delete-contact/<str:group_key>/<str:contact_key>/', removeuserFromGroup, name='group-delete'),
]
