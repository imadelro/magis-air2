from django.contrib import admin

from .models import *

# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    model = Flight

class CityAdmin(admin.ModelAdmin):
    model = City

class FlightScheduleAdmin(admin.ModelAdmin):
    model = FlightSchedule

class FlightTicketInline(admin.TabularInline):
    model = FlightTicket

class AdditionalItemAdmin(admin.ModelAdmin):
    model = AdditionalItem

class ItemOrderInline(admin.TabularInline):
    model = ItemOrder

class FlightBookingAdmin(admin.ModelAdmin):
    model = FlightBooking
    inlines = [FlightTicketInline, ItemOrderInline]

class CrewAssignmentInline(admin.TabularInline):
    model = CrewAssignment

class CrewAdmin(admin.ModelAdmin):
    model = CrewMember
    inlines = [CrewAssignmentInline]

admin.site.register(City, CityAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(AdditionalItem, AdditionalItemAdmin)
admin.site.register(FlightSchedule, FlightScheduleAdmin)
admin.site.register(FlightBooking, FlightBookingAdmin)
admin.site.register(CrewMember, CrewAdmin)
