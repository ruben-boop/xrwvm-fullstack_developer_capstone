# Uncomment the following imports before adding the Model code

from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


# Create CarModel
class CarModel(models.Model):

    car_make = models.ForeignKey(CarMake,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('PICKUP', 'Pickup'),
        ('JEEP', 'Jeep'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=11, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2024,
                               validators=[
                                   MaxValueValidator(2024),
                                   MinValueValidator(2015)
                                ])
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name  # Return the name as the string representation

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=50)

class Review(models.Model):
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    review = models.TextField()
    sentiment = models.CharField(max_length=10)  # positive, negative, neutral
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    date = models.DateField()
