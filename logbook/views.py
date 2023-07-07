from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from .models import Employee, Department
from .forms import EmployeeForm, EditPersonalInfoForm
from django import forms


def main_page(request):
    return render(request, 'main_page.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def employee_list(request):
    departments = Department.objects.all()
    employees_per_department = 2
    paginator = Paginator(departments, employees_per_department)
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    context = {
        'page_obj': page_obj
    }
    return render(request, 'employee_list.html', context)


class EditPersonalInfoForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

@login_required
def edit_personal_info(request):
    user = request.user
    try:
        employee = user.employee  # Retrieve the associated Employee instance
    except Employee.DoesNotExist:
        # Handle the case where the user doesn't have an Employee record
        # For example, redirect to a different page or display an error message
        return redirect('employee_list')

    if request.method == 'POST':
        form = EditPersonalInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if email:
                user.email = email
                user.save()

            if password:
                user.set_password(password)
                user.save()

            return redirect('employee_list')
    else:
        form = EditPersonalInfoForm(initial={'email': user.email})

    return render(request, 'edit_personal_info.html', {'form': form})

@login_required
def employee_management(request):
    if not request.user.is_staff:
        # If the user is not a staff member, redirect them to a different page
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_management')
    else:
        form = EmployeeForm()

    # Retrieve the list of active employees
    employees = Employee.objects.filter(is_active=True)

    return render(request, 'employee_management.html', {'form': form, 'employees': employees})
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_management')  # Redirect to the employee management page after adding the employee
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})
@login_required
def update_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    departments = Department.objects.all()  # Retrieve all departments

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_management')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'update_employee.html', {'form': form, 'departments': departments})

@login_required
def confirm_delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'confirm_delete_employee.html', {'employee': employee})

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
    return redirect('employee_management')