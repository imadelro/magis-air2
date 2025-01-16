from django.urls import path
from .views import *

urlpatterns = [
    path('', PassengerDetailView.as_view(), name='passenger-detail'),
    path('update', PassengerUpdateView.as_view(), name='passenger-update'),
    path('create', PassengerCreateView.as_view(), name='passenger-create'),
    # path('<int:pk>/create', PassengerCreateView.as_view(), name='passenger-create'),
]

app_name = 'user_management'