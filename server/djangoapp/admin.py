from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review

# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):

    model = CarModel
    extra = 2


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):

    inlines = [CarModelInline]
    list_display = ['name', 'description']


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):

    list_display = ['car_make', 'name', 'type', 'year', 'color']
    list_filter = ['car_make']
    search_fields = ['car_make', 'name', 'type']


# DealerAdmin class
class DealerAdmin(admin.ModelAdmin):

    list_display = ['id', 'full_name', 'city', 'state', 'zip']
    list_filter = ['state']
    search_fields = ['full_name', 'city', 'state']


# ReviewAdmin class
class ReviewAdmin(admin.ModelAdmin):

    list_display = ['id', 'dealership', 'name', 'sentiment', 'date']
    list_filter = ['sentiment', 'date', 'dealership']
    search_fields = ['name', 'review', 'car_make', 'car_model']


# Registering models with their respective admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Review, ReviewAdmin)
