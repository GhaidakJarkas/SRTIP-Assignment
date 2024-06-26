from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
from core.models import Customer
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from core.forms import CustomerForm
from core.decorators import allowed_users
from cities_light.models import Country, City
from django.http import JsonResponse 
from core.forms import SubscriptionForm
from core.models import Plan

import datetime


#Index page
def index(request):
    return render(request, "core/index.html")


#Login function
def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    else:

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email, password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('core:index')
            else:
                messages.error(request, "Email or Password is incorrect", extra_tags="danger")
                return redirect('core:login')
        return render(request, "core/login.html")
    

#User Logout Function
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('core:login')


#List of all users
#Only Admin users are allowed to see this page
@allowed_users(['admin'])
def users(request):
    users = CustomUser.objects.all().order_by('-created_at')
    ctx = {
        "users": users
    }

    return render(request, "core/users.html", ctx)


#Create new user
#Only Admin users are allowed to see this page
@allowed_users(['admin'])
def create_user(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = CustomUserCreationForm(data)
        
        if form.is_valid():
            form.save()
            messages.success(request, "User has been created successfully")
            return redirect('core:users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in the {field} Field: {error}", extra_tags='danger')

            ctx = {
                "customuser": data
            }
            return render(request, "core/create-user.html", ctx)
            
    return render(request, "core/create-user.html")


#Edit a user
#Only Admin users are allowed to see this page
@allowed_users(['admin'])
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        data = request.POST.copy()
        print(data)
        form = CustomUserChangeForm(data, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User has been updated successfully")
            return redirect('core:users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f"Error in the {field} Field: {error}", extra_tags='danger')

            data['pk'] = user.pk
            ctx = {
                'customuser': data
            }
            return render(request, 'core/edit-user.html', ctx)

    ctx = {
        'customuser': user
    }
    return render(request, "core/edit-user.html", ctx)



#Delete a user
#Only Admin users are allowed to see this page
@allowed_users(['admin'])
def delete_user(request):
    data = request.POST.copy()
    user = get_object_or_404(CustomUser, pk=data.get('userid'))
    user.delete()
    messages.success(request, "User has been deleted successfully")
    return redirect('core:users')



#List of all customers
#All users are allowed to see this page
@allowed_users(['admin', 'staff', 'customer'])
def customers(request):
    customers = Customer.objects.all().order_by('-created_at')
    ctx = {
        'customers': customers
    }
    return render(request, 'core/customers.html', ctx)



#Create new customer
#All users are allowed to see this page
@allowed_users(['admin', 'staff', 'customer'])
def create_customer(request):
    countries = Country.objects.all().values('pk', 'name')
    ctx = {
        "countries": countries
    }
    if request.method == 'POST':
        data = request.POST.copy()
        print(data)
        form = CustomerForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been created successfully")
            return redirect('core:customers')
        else: 
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in the {field} Field: {error}", extra_tags='danger')
            try:
                dob_str = data.get('dob') 
                dob_date = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
                data['dob'] = dob_date
            except:
                pass
            ctx['customer'] = data
            return render(request, "core/create-customer.html", ctx)
    return render(request, "core/create-customer.html", ctx)


#Edit a customer
#Only Admin and Staff users are allowed to see this page
@allowed_users(['admin', 'staff'])
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    countries = Country.objects.all().values('pk', 'name')
    if request.method == 'POST':
        data = request.POST.copy()
        form = CustomerForm(data, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been updated successfully")
            return redirect('core:customers')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in the {field} Field: {error}", extra_tags='danger')
            
    ctx = {
        'customer': customer,
        'countries': countries
    }
    return render(request, "core/edit-customer.html", ctx)



#Delete a customer
#Only Admin users are allowed to see this page
@allowed_users(['admin'])
def delete_customer(request):
    data = request.POST.copy()
    customer = get_object_or_404(Customer, pk=data.get('customerid'))
    customer.delete()
    messages.success(request, "Customer has been deleted successfully")
    return redirect('core:customers')


#Get a list of a country's cities
def get_cities(request, id):
    cities = City.objects.filter(country=id).values('pk', 'name')
    cities = list(cities)
    return JsonResponse(data={"cities": cities}, status=200)



from core.models import Subscription
#Get a list of all subscription
@allowed_users(['staff', 'admin'])
def subscriptions(request):
    
    if request.user.role == 'staff':
        subscriptions = Subscription.objects.filter(verified=False)
    elif request.user.role == 'admin':
        subscriptions = Subscription.objects.filter(verified=True)

    ctx = {
        'subscriptions': subscriptions
    }

    return render(request, "core/subscriptions.html", ctx)


def subscription_details(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    ctx = {
        'subscription': subscription
    }

    return render(request, "core/subscription-details.html", ctx)


def verify_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if not subscription.verified and request.user.role == 'staff':
        subscription.verified = True
        subscription.save()
        return JsonResponse(data={"message": "This request has been approved successfully"}, status=200)
    return render(request, "404.html")
    





def create_subscription(request):
    plans = Plan.objects.filter(status=True)
    if request.method == 'POST':    
        data = request.POST.copy()
        doc = request.FILES

        form = SubscriptionForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your data has been submitted successfully")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in the {field} Field: {error}", extra_tags='danger')
            ctx = {
                'subscription': data,
                'plans': plans
            }

            return render(request, "core/subscription.html", ctx)

    ctx = {
            'plans': plans
        }
    return render(request, "core/subscription.html", ctx)