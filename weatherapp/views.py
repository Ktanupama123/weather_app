from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages
import requests
import datetime
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def signupview(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        print(username,"llllllllllllll")
        print(email)
        print(password)
        print(confirm_password)
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,'email is already taken') 
        if password!=confirm_password:
            messages.error(request,'password is not same')
            return redirect('signup')
        user= CustomUser.objects.create_user(email=email,username=username,password=password)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'signup.html')
def signinview(request):
    if request.method=='POST':
        user_name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=user_name,password=password)
        if user is not None :
            login(request,user)
            messages.success(request,'Login successfull')
            return redirect('home')
        else:
            messages.error(request,'incorrect password')
            return redirect('login')
    return render(request,'signin.html')
def homeview(request):
    print('user',request.user)
    return render(request,'home.html',{'user':request.user})
def signoutview(request):   
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
@login_required(login_url='login')
def weather(request):
    print('user',request.user)
    if 'city' in request.POST:
        city=request.POST.get('city')
    else:
        city='calicut' 
    APP_ID = os.getenv('APP_ID')
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}"
    PARAMS={'units':'metric'}


    try:
        data= requests.get(url,params=PARAMS).json()
        description=data['weather'][0]['description']
        icon=data['weather'][0]['icon']
        temp=data['main']['temp']
        day=datetime.date.today()

        return render(request,'weather.html',{
            'description':description,
            'icon':icon,
            'temp':temp,
            'day':day,
            'city':city,
            'exception_occurred':False,

        })
    except KeyError:
        exception_occurred=True
        messages.error(request,'Entered data is not available to API')
        day=datetime.date.today()
    return render(request,'weather.html',{
        'description':'clear sky',
        'icon':'01d',
        'temp':25,
        'day':day,
        'city':'calicut',
        'exception_occurred':exception_occurred,
    })