from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('createUser/', views.createUser),
    path('login/', views.login),
    path('logout/', views.logout),
    path('travels/', views.travels),
    path('travels/destination/<int:planid>/', views.destination),
    path('travels/joinTrip/<int:planid>/', views.joinTrip),
    path('travels/add/', views.addTravel),
    path('travels/add/addPlan/', views.addTripPlan),
]