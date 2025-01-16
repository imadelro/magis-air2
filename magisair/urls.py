from django.urls import path
from .views import *


urlpatterns = [
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('flights/schedule/', FlightScheduleSearchView.as_view(), name='flight_schedule_search'),
    path('flights/<pk>/', FlightDetailView.as_view(), name='flight_detail'),

]

app_name = 'magisair'