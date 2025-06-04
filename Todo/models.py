from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# function to validate the file size which is being uploaded
def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size should not exceed 5 MB. Please upload a valid file")

# Task Model representing the fields which are present for a todo-task addition.
class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    deadline = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], default="Low")
    completed = models.BooleanField(default=False)
    recurrence = models.CharField(max_length=20, choices=[("None", "None"), ("Daily", "Daily"), ("Weekly", "Weekly"), ("Monthly", "Monthly")], default="None")
    shared_with = models.ManyToManyField(User, related_name="shared_tasks", blank=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True, validators=[validate_file_size])
    progress = models.CharField(max_length=20, choices=[("Not Started", "Not Started"), ("In Progress", "In Progress"), ("Completed", "Completed")], default="Not Started")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # the overdue task would be displayed when the time condigured is passed out and whenn the task is not completed
    def is_overdue(self):
        """Returns True if the task deadline has passed and it's not completed."""
        return not self.completed and self.deadline < timezone.now()

    def __str__(self):
        return self.title
