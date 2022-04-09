from django.urls import path 
from . import views


urlpatterns = [
    path('', views.send_the_homepage),
    path('login/', views.log_in),
    path('whoami/', views.who_am_i),
    path('logout/', views.log_out)
]