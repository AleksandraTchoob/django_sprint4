from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.SignUp.as_view(), name='signup'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/',
         views.profile_edit, name='profile_edit'),
]
