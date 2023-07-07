# logbook/forms.py
from django import forms
from django.contrib.auth.models import User

from .models import Employee


from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'mobile_phone', 'work_phone', 'email', 'occupation', 'department')
        widgets = {
            'department': forms.Select(attrs={'required': True}),
        }


class EditPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
