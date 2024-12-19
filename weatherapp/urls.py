from django.urls import path
from  .import views

urlpatterns =[
    path('signup/',views.signupview,name='signup'),
    path('login/',views.signinview,name='login'),
    path('',views.homeview,name='home'),
    path('signout/', views.signoutview, name='signout'),
    path('weather/',views.weather,name='weather')


]
