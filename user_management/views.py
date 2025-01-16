from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Passenger
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from magisair.models import *

class PassengerUpdateView(LoginRequiredMixin, UpdateView):
    model = Passenger
    form_class = PassengerUpdateForm
    template_name = 'passenger_update.html'

    def get_object(self):
        return Passenger.objects.get(user__pk=self.request.user.pk)

    def get_success_url(self) -> str:
        return reverse_lazy("passenger:passenger-detail", kwargs={"pk": self.object.pk})


class PassengerDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'passenger_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Passenger.objects.filter(user__pk=self.request.user.pk).exists():
            return {'passenger': Passenger.objects.get(user__pk=self.request.user.pk)}
        return context
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context == super().get_context_data(**kwargs):
            return redirect('user_management:passenger-create')
        return super().dispatch(request, *args, **kwargs)


class PassengerCreateView(LoginRequiredMixin, CreateView):
    model = Passenger
    form_class = PassengerCreateForm
    template_name = 'passenger_create.html'
    def dispatch(self, request, *args, **kwargs):
        if Passenger.objects.filter(user__pk=self.request.user.pk).exists():
            return redirect('user_management:passenger-detail')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        if form.is_valid():
            passenger=Passenger()
            passenger.user=self.request.user
            # passenger.passport_id
            passenger.first_name=form.cleaned_data.get('first_name')
            passenger.middle_name=form.cleaned_data.get('middle_name')
            passenger.email=form.cleaned_data.get('email')
            passenger.last_name=form.cleaned_data.get('last_name')
            passenger.birth_date=form.cleaned_data.get('birth_date')
            passenger.gender=form.cleaned_data.get('gender')
            passenger.user.user_id=form.cleaned_data.get('user_id')
            passenger.save()
        return redirect('magisair:flight_list')
    

    def get_success_url(self) -> str:
        return reverse('flight_list')
