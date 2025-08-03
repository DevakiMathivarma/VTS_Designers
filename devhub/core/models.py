from django.contrib.auth.models import AbstractUser
from django.db import models

# Extended User
class PythonUser(AbstractUser):
    
    location = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    projects_descriptions = models.TextField(blank=True)  # Combined summary
    custom_message = models.CharField(max_length=255, blank=True)
    hired_users = models.ManyToManyField('self', symmetrical=False, related_name='hired_by', blank=True)
    can_add_projects = models.BooleanField(default=True)  # For view-only users

# Projects
class Project(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published')
    ]
    CATEGORY_CHOICES = [
         ('', 'Select category'),
        ('UI', 'UI Design'),
        ('WEB', 'Web Design'),
        ('APP', 'App Design'),
        ('GRAPHIC', 'Graphic Design'),
    ]

    LICENSE_CHOICES = [
        ('ALL_RIGHTS', 'All Rights Reserved'),
        ('CC', 'Creative Commons'),
        ('MIT', 'MIT License'),
    ]
    owner = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='projects')
    images = models.ImageField(upload_to='projects/', blank=True, null=True)
    project_title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True,  
    null=True)
    license = models.CharField(max_length=50, choices=LICENSE_CHOICES, default='ALL_RIGHTS')
    description = models.TextField(max_length=100)
    tags = models.CharField(max_length=200, blank=True)
    visibility = models.CharField(max_length=20, choices=[('Public', 'Public'), ('Private', 'Private')], default='Public')
    downloadable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)


    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
# Hiring
class HiringPost(models.Model):
    user = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='hiring_posts')
    reason_for_hire = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    project_description = models.TextField()
    personal_note = models.TextField(blank=True)
    hiring_for = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

# Messages
class Message(models.Model):
    sender = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Notifications
class Notification(models.Model):
    sender = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)  # new field

    user = models.ForeignKey(PythonUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
