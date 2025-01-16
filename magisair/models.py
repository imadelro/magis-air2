from django.db import models
from django.db.models import F, DurationField, ExpressionWrapper
from user_management.models import Passenger
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
# Create your models here.

class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Cities'

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, primary_key=True, validators=[alphanumeric], null=False)
    origin_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure_flights')
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrival_flights')
    flight_type = models.CharField(choices=[('N', 'Non-stop Flight'), ('D', 'Direct Flight')], max_length=20)

    def __str__(self):
        return str(self.flight_number)

class FlightSchedule(models.Model):
    schedule_id = models.CharField(max_length=10,primary_key=True, validators=[alphanumeric], null=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='schedules', null=False)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    @property
    def duration(self):
        return self.arrival - self.departure
    def __str__(self):
        return f'{str(self.flight.flight_number)} {str(self.departure)}'

class FlightBooking(models.Model):
    reference_number = models.IntegerField(primary_key=True,null=False,validators=[alphanumeric])
    booking_date = models.DateField()
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    @property
    def total_cost(self):
        return sum([ticket.cost for ticket in self.tickets.all()]) + sum([item.cost for item in self.additional_items.all()])
    def __str__(self):
        return str(self.reference_number)

class FlightTicket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True, validators=[alphanumeric],null=False)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    seat = models.CharField(max_length=5, validators=[alphanumeric])
    booking = models.ForeignKey(FlightBooking, on_delete=models.CASCADE, related_name='tickets')
    schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE, related_name='tickets')

class AdditionalItem(models.Model):
    item_id = models.CharField(max_length=10, primary_key=True,null=False)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.description)

class ItemOrder(models.Model):
    booking = models.ForeignKey(FlightBooking, on_delete=models.CASCADE, related_name="additional_items")
    item = models.ForeignKey(AdditionalItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    @property
    def cost(self):
        return self.quantity * self.item.cost

class CrewMember(models.Model):
    employee_id = models.IntegerField(primary_key = True, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{str(self.first_name)} {str(self.last_name)}'

class CrewAssignment(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    flight_schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.crew)} {str(self.flight_schedule)}'
