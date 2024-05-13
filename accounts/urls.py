from django.urls import path
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.users, name='users'),
    path('create-user', views.create_user, name='create-user'),
]