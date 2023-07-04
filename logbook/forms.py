from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['mobile_phone']
        widgets = {
            'mobile_phone': forms.TextInput(attrs={'class': 'form-control'})
        }
