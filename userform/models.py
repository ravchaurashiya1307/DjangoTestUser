from django.db import models
from django import forms

class NewUser(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='pics/')
class NewForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['name', 'dob','email','phone', 'image']
