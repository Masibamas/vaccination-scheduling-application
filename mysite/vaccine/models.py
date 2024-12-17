from django.db import models

# Create your models here.

class Vaccine(models.Model):
    name = models.CharField("Vaccine Name", max_length=32)
    description = models.TextField(max_length=1024)
    number_of_doses = models.IntegerField(default=1)
    interval = models.IntegerField(default=0, help_text='Please Provide interval in days')
    storage_temprature = models.IntegerField(null=True, blank=True, help_text="Provide temprature in celcius")
    minimum_age= models.IntegerField(default=0)


    def __str__(self):
        return self.name
