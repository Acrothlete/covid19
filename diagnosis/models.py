from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"), ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"), ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"), ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"), ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"), ("Odisha", "Odisha"),
                 ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"), ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"), ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"), ("Lakshadweep", "Lakshadweep"), ("National Capital Territory of Delhi", "National Capital Territory of Delhi"), ("Puducherry", "Puducherry"))
fever_choice = (
    ('0', 'No Fever (98*F)'),
    ('1', 'Mild Fever (100*F)'),
    ('3', 'High Fever (103*F)'),
)

travel_choice = (
    ('0', 'None'),
    ('1', 'National'),
    ('2', 'International'),
    ('5','Covid Infected Zone '),
)

class data_base(models.Model):
    name = models.CharField(max_length=128, blank=False)
    phone = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,10}$')], blank=False)
    age = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    city=models.CharField(max_length=100,blank=False)
    state=models.CharField(max_length=128,blank=False)
    travelHistory=models.CharField(max_length=128,choices=travel_choice,blank=False)
    fever=models.CharField(max_length=128,choices=fever_choice,blank=False)
    bodyPain=models.IntegerField(default=0)
    runningNose=models.IntegerField(default=0)
    difficulty_Breathing=models.IntegerField(default=0)
    soreThroat=models.IntegerField(default=0)
    infectionProb=models.FloatField(default=0)
    date=models.DateTimeField(default=timezone.now)

patient_choice = (
    ('Positive', 'Positive'),
    ('Saspected', 'Saspected'),
    ('Nagetive', 'Nagetive'),
)

class Patient_data(models.Model):
    name = models.CharField(max_length=128, blank=False)
    age = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    city=models.CharField(max_length=100,blank=False)
    state=models.CharField(max_length=128,blank=False)
    patient_status=models.CharField(max_length=20,choices=patient_choice,blank=False)
    date=models.DateTimeField(default=timezone.now)




    
    