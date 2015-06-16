from django import forms
from django.forms.widgets import Textarea
from django.core.mail import send_mail, BadHeaderError

from .models import *

class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields='__all__'
        
class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields='__all__'

class InvitationForm(forms.ModelForm):
    class Meta:
        model=Invitation
        exclude=['password']

class MealForm(forms.ModelForm):
    class Meta:
        model=Meal
        widgets={
            'starter': forms.RadioSelect(),
            'main': forms.RadioSelect(),
            'dessert': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(MealForm,self).__init__(*args, **kwargs)

        for course,course in MealOption.COURSE_CHOICES:
            self.fields[course].queryset=MealOption.objects.filter(course=course)
            self.fields[course].empty_label=None

class ContactForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    subject=forms.CharField()
    message=forms.CharField(widget=Textarea())