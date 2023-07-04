from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from .models import Employee
from .forms import EmployeeForm


def main_page(request):
    return render(request, 'main_page.html')


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_list')  # Redirect to the employee list page
        else:
            # Authentication failed, handle the error (e.g., show an error message)
            pass
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def employee_list(request):
    employees = Employee.objects.all()  # Fetch all employees from the database
    context = {'employees': employees}  # Create a context dictionary with the employees
    return render(request, 'employee_list.html', context)


@login_required
def edit_personal_info(request):
    current_user = request.user
    employee = current_user.employee

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal information updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    context = {'form': form}
    return render(request, 'edit_personal_info.html', context)


@login_required
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list')
