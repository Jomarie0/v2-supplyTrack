# supplytrack/users/views.py
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm

# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type (Manager or Staff)
                if user.groups.filter(name='Manager').exists():
                    return redirect('dashboard:home')  # Redirect to Manager dashboard
                else:
                    return redirect('inventory:inventory_list')  # Redirect to Staff inventory list
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

# Register view
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
            else:
                # Create the user
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Assign the user to a group (Staff or Manager)
                try:
                    if "manager" in username.lower():
                        manager_group = Group.objects.get(name='Manager')
                        user.groups.add(manager_group)
                    else:
                        staff_group = Group.objects.get(name='Staff')
                        user.groups.add(staff_group)
                except Group.DoesNotExist:
                    # If groups don't exist, create them
                    manager_group, created = Group.objects.get_or_create(name='Manager')
                    staff_group, created = Group.objects.get_or_create(name='Staff')
                    if "manager" in username.lower():
                        user.groups.add(manager_group)
                    else:
                        user.groups.add(staff_group)

                messages.success(request, "Account created successfully! Please log in.")
                return redirect('users:login')  # Redirect to the login page after registration
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('users:login')  # Redirect to the login page after logout
