from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Q
import logging
from .models import Post
from .forms import TodoForm, CustomUserCreationForm
from django.contrib.auth.views import PasswordResetConfirmView

# Set up logger
logger = logging.getLogger(__name__)

# Password Reset Custom View
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        logger.info(f"Password updated for user: {user.username}")
        messages.success(self.request, "Your password has been successfully updated.")
        return super().form_valid(form)

# Task listed in Todo view page.
@login_required
def Todo_list(request):
    #User can filter the task based on the category
    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")

    todos = Post.objects.filter(user=request.user)

    if search_query:
        todos = todos.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if category_filter:
        todos = todos.filter(category=category_filter)

    # The overdue tasks would be listed here. The deadline and completion status would be checked and the corresponding data would be displayed
    overdue_tasks = todos.filter(deadline__lt=now(), completed=False)

    if overdue_tasks.exists():
        messages.warning(request, f"You have {overdue_tasks.count()} overdue tasks!")

    context = {
        "Todo_list": todos,
        "overdue_tasks": overdue_tasks,
        "search_query": search_query,
        "category_filter": category_filter,
    }
    return render(request, "Todo/Todo_list.html", context)

# User registration function works here, where when the user clicks the submit button, the function check for the all the details and if it is correct, user registartion would be successfull and redirected towards the login page for login.
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, "Registration successful! You can now proceed with log in phase")
            return redirect('Todo:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Todo/register.html', {'form': form})

    # User Login View, checks the authentication with the provided username and password , if the crednetials are right, the page would be redirected to dashboard.
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('Todo:todo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'Todo/login.html', {'form': form})

# On click of the logout button, the funtion is implemented and let the user log out the application.
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('Todo:login')

# On click of the logout button, the funtion is implemented and let the user log out the application.
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('Todo:login')

# add task function is implemented here.
@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            # added task is associated with the user who performed this action.
            todo.user = request.user
            todo.save()
            messages.success(request, "Task added successfully!")
            return redirect('Todo:todo_list')
    else:
        form = TodoForm()
    return render(request, 'Todo/add_todo.html', {'form': form})

# modification of the existing task
@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(Post, id=todo_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('Todo:todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'Todo/edit_todo.html', {'form': form})

# On click od 'delete' action button, the function would be called and the task deletion would take place.
@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Post, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('Todo:todo_list')
    return render(request, 'Todo/delete_todo.html', {'todo': todo})

# if the user click the 'mark as completed' , the function would be called for execution. The status would be marked pending in else conditions.
@login_required
def toggle_complete(request, todo_id):
    todo = get_object_or_404(Post, id=todo_id, user=request.user)
    # Toggle the completed status
    todo.completed = not todo.completed
    todo.save()
    status = "completed" if todo.completed else "pending"
    messages.success(request, f"Task marked as {status}.")
    return redirect('Todo:todo_list')

# Recurring Tasks View
@login_required
def recurring_tasks(request):
    recurring_todos = Post.objects.filter(user=request.user, recurrence__in=["Daily", "Weekly", "Monthly"])
    context = {
        'recurring_todos': recurring_todos,
    }
    return render(request, 'Todo/recurring_tasks.html', context)
