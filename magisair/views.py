from django.urls import reverse_lazy, reverse
from django.utils.dateparse import parse_date
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.utils.timezone import now
from django.utils import timezone

from django.utils import timezone

class FlightListView(ListView):
    model = Flight
    template_name = "flight_list.html"
    context_object_name = 'flights'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.localtime(timezone.now())
        context['current_time'] = current_time

        flight_type = self.request.GET.get('flight_type')

        if flight_type:
            context['flights'] = Flight.objects.filter(flight_type=flight_type)
        else:
            context['flights'] = Flight.objects.all()

        for flight in context['flights']:
            flight.future_schedules = flight.schedules.filter(departure__gt=timezone.now())

        return context
class FlightDetailView(DetailView):
    model = Flight
    template_name = "flight_detail.html"
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['additional_items'] = AdditionalItem.objects.all()

        return context 

class BookingListView(ListView):
    model = FlightBooking
    template_name = "list_bookings.html"

class CreateBookingView(LoginRequiredMixin, CreateView):
    model = FlightBooking
    template_name = "create_booking.html"
    form_class = BookingCreateForm
    def get_success_url(self):
        return reverse_lazy('magisair:list_bookings')
    def get_form(self, form_class=None):
        passenger = Passenger.objects.get(user=self.request.user)
        form = super().get_form(form_class)
        form.fields['passenger'].choices = [(passenger.passport_id, str(passenger))]
        form.fields['passenger'].widget.attrs['disabled'] = True
        return form
    
class BookingDetailView(DetailView):
    model = FlightBooking
    template_name = "booking_detail.html"

class UpdateBookingView(UpdateView):
    model = FlightBooking
    template_name = "update_booking.html"

class DeleteBookingView(DeleteView):
    model = FlightBooking
    template_name = "delete_booking.html"


class FlightScheduleSearchView(ListView):
    model = FlightSchedule
    template_name = "flight_schedule_search.html"
    context_object_name = 'flight_schedules'

    def get_queryset(self):
        queryset = FlightSchedule.objects.all()

        origin = self.request.GET.get('origin')
        destination = self.request.GET.get('destination')
        date = self.request.GET.get('date')

        if origin:
            queryset = queryset.filter(flight__origin_city__name__icontains=origin)

        if destination:
            queryset = queryset.filter(flight__destination_city__name__icontains=destination)

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(departure__date=parsed_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['origin'] = self.request.GET.get('origin', '')
        context['destination'] = self.request.GET.get('destination', '')
        context['date'] = self.request.GET.get('date', '')
        return context