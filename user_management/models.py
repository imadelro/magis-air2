from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # is this allowed
    passport_id = models.CharField(max_length=10, primary_key=True, validators=[alphanumeric])
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(choices=[('F', 'Female'), ('M','Male')], max_length=1)

    def __str__(self):
        return f'{str(self.last_name)}, {str(self.first_name)} {str(self.middle_name)[0]}.'

    def get_absolute_url(self):
        return reverse("passenger:passenger-detail", kwargs={"pk": (self.passport_id)})


