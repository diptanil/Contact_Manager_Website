from django.urls import path
from .views import UserSignup, UserLogin, UserView, UserLogout

urlpatterns = [
    path('signup/', UserSignup.as_view()),
    path('login/', UserLogin.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', UserLogout.as_view())
]

