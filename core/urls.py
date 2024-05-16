from django.urls import path 
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),

    #Auth
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    #Users
    path('users/', views.users, name='users'),
    path('create-user', views.create_user, name='create-user'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit-user'),
    path('delete-user/', views.delete_user, name='delete-user'),

    #Customers
    path('customers/', views.customers, name='customers'),
    path('create-customer/', views.create_customer, name='create-customer'),
    path('edit-customer/<int:pk>/', views.edit_customer, name='edit-customer'),
    path('delete-customer/', views.delete_customer, name='delete-customer'),
    path('get-cities/<int:id>/', views.get_cities, name='get-cities'),


    #Subscription
    path('create-subscription/', views.create_subscription, name='create-subscription'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscription-details/<int:pk>/', views.subscription_details, name='subscription-details'),
    path('verify-subscription/<int:pk>/', views.verify_subscription, name='verify-subscription'),
]