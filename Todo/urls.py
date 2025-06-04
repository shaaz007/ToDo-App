from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    Todo_list,
    register_user,
    login_user,
    logout_user,
    add_todo,
    edit_todo,
    delete_todo,
    toggle_complete,
    recurring_tasks,
    CustomPasswordResetConfirmView,
)

# The app name is mentioned here
app_name = 'Todo'

urlpatterns = [
    # Navigation for the tasks whihc are being added, modified and deleted.  The class which has to be executed on the redirection is also mentioned.
    path('', Todo_list, name='todo_list'),
    path('add/', add_todo, name='add_todo'),
    path('edit/<int:todo_id>/', edit_todo, name='edit_todo'),
    path('delete/<int:todo_id>/', delete_todo, name='delete_todo'),
    path('complete/<int:todo_id>/', toggle_complete, name='toggle_complete'),
    path('recurring/', recurring_tasks, name='recurring_tasks'),

    # User authentication navigations.
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Password Reset Views
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),  # Use custom view
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
