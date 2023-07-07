from django.urls import path
from django.contrib.auth import views as auth_views
from logbook import views

urlpatterns = [
    # Other URL patterns...
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('login/', views.login_view, name='login'),

]
