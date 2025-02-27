from django.db import models
from django.contrib.auth.models import User

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.company_name


class SmartBin(models.Model):
    BIN_TYPES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
    ]

    bin_type = models.CharField(max_length=20, choices=BIN_TYPES)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True) 
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.IntegerField() 
    current_fill_level = models.IntegerField()  
    detected_waste_type = models.CharField(max_length=20, choices=BIN_TYPES)
    fill_status = models.CharField(max_length=20)  
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Call the method to calculate fill status before saving
        self.calculate_fill_status()
        super().save(*args, **kwargs)

    def calculate_fill_status(self):
        if self.current_fill_level >= 75:
            self.fill_status = 'red'
        elif self.current_fill_level >= 40:
            self.fill_status = 'yellow'
        else:
            self.fill_status = 'green'

    def __str__(self):
        return f"Bin {self.id} ({self.bin_type}) at {self.location}"


class Vehicle(models.Model):
    VEHICLE_STATUS = [
        ('idle', 'Idle'),
        ('en route', 'En Route'),
        ('collecting', 'Collecting'),
    ]

    vehicle_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=VEHICLE_STATUS)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vehicle {self.vehicle_id} - {self.status}"


class DumpingArea(models.Model):
    WASTE_TYPES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
    ]

    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    quantity = models.IntegerField()  # Quantity in kilograms
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.waste_type.capitalize()} Waste - {self.quantity} kg"


class Company(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=200)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WastePurchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(DumpingArea, on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField()  # Quantity in kilograms
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.quantity_purchased} kg of {self.waste_type.waste_type}"