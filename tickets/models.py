from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('USER', 'End User'),
    ('ENGINEER', 'Support Engineer'),
    ('ADMIN', 'Administrator'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Ticket(models.Model):
    STATUS_CHOICES = (('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'))
    CATEGORY_CHOICES = (('Hardware', 'Hardware'), ('Software', 'Software'), ('Network', 'Network'), ('Other', 'Other'))
    # NEW: Priority Levels
    PRIORITY_CHOICES = (('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'))

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.title}"

# NEW: Comment System
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"