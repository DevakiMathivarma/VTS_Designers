from django.shortcuts import render
from .models import Project, Message, Notification, HiringPost, PythonUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HiringPost, PythonUser, Notification
from .forms import HiringPostForm
from .models import PythonUser, Message  # Assuming you have a Message model
from .forms import MessageForm  
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q
from django.db.models import Q, Max
from .models import Message, PythonUser
from django.http import JsonResponse
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project
from django.shortcuts import redirect
User = get_user_model()

@login_required
def notifications_context(request):
    if request.user.is_authenticated:
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        notifications_count = recent_notifications.count()
        return {
            'recent_notifications': recent_notifications,
            'notifications_count': notifications_count
        }
    return {}

@login_required
def dashboard(request):

    recent_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')[:5]
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    available_candidates = PythonUser.objects.exclude(id=request.user.id).filter(can_add_projects=True)[:5]  # Adjust filter
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.status = 'Published'
            project.save()
            messages.success(request, "Project uploaded successfully!")
            return redirect('dashboard')
        
    category_placeholder = Project.objects.values_list('category', flat=True).first() or "Enter category"

    context = {
        'total_projects': request.user.projects.count(),  # Example if you have a related_name
        'messages_count': recent_messages.count(),
        'candidates_count': available_candidates.count(),
        'notifications_count': recent_notifications.count(),
        'recent_messages': recent_messages,
        'recent_notifications': recent_notifications,
        'available_candidates': available_candidates,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def project_create(request):
    published_project = None
    recent_projects = None
    edit_mode = False
    project_to_edit = None

    if request.method == 'POST':
        if 'edit_mode' in request.POST:  # user clicked "Edit Projects"
            project_id = request.POST.get('project_id')
            project_to_edit = Project.objects.get(id=project_id, owner=request.user)
            form = ProjectForm(instance=project_to_edit)
            recent_projects = Project.objects.filter(owner=request.user).order_by('-created_at')[:4]
            edit_mode = True
        else:
            project_id = request.POST.get('project_id')
            if project_id:  # editing existing project
                project_to_edit = Project.objects.get(id=project_id, owner=request.user)
                form = ProjectForm(request.POST, request.FILES, instance=project_to_edit)
            else:  # creating new project
                form = ProjectForm(request.POST, request.FILES)
            
            if form.is_valid():
                project = form.save(commit=False)
                project.owner = request.user
                if 'publish' in request.POST:
                    project.status = 'Published'
                else:
                    project.status = 'Draft'
                project.save()
                published_project = project
                form = None  # hide form
    else:
        form = ProjectForm()
        recent_projects = Project.objects.filter(owner=request.user).order_by('-created_at')[:4]

    return render(request, 'core/project_create.html', {
        'form': form,
        'published_project': published_project,
        'recent_projects': recent_projects,
        'edit_mode': edit_mode,
        'project_to_edit': project_to_edit
    })


@login_required
def hire_now(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project_owner = project.owner  # Project owner's user object
    print("POST2 request received!")  # <---- Add this to verify

    if request.method == "POST":  # Only send email on form submit
        print("POST request received!")  # <---- Add this to verify

        reason_for_hire = request.POST.get("reason_for_hire")
        category = request.POST.get("category")
        budget = request.POST.get("budget")
        project_description = request.POST.get("project_description")
        personal_note = request.POST.get("personal_note")
        hiring_for = request.POST.get("hiring_for")

        # Build email content
        subject = f"Hiring Request from {request.user.username}"
        message = f"""
Hello {project_owner.username},

You have a new hiring request for your project: {project.project_title}

Details:
- Reason for Hire: {reason_for_hire}
- Category: {category}
- Budget: {budget}
- Project Description: {project_description}
- Personal Note: {personal_note}
- Hiring For: {hiring_for}

From: {request.user.username} ({request.user.email})
"""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [project_owner.email],  # Send to project owner's email
                fail_silently=False,
            )
            print("Email sent successfully to:", project_owner.email)
            messages.success(request, "Your hiring request has been sent!")
        except Exception as e:
            print("Email sending failed:", e)
            messages.error(request, "Failed to send the email. Please try again later.")
        
        return redirect('dashboard')  # After sending, redirect

    # On GET, just render the page
    return render(request, 'core/hire_now.html', {'project_id': project_id, 'target_user': project_owner})






@login_required
def project_view(request, pk):
    project = Project.objects.get(pk=pk)
    project.views += 1
    project.save()
    if request.method == "POST" and 'edit_mode' in request.POST:
        form = ProjectForm(instance=project)
        return render(request, 'core/project_create.html', {
            'published_project': None,  # hide preview
            'edit_mode': True,
            'form': form,
            'recent_projects': Project.objects.filter(owner=request.user).order_by('-created_at')[:4],
            'project_to_edit': project
        })
    return render(request, 'core/project_create.html', {
        'published_project': project,
        'edit_mode': False,
        'form': None,
        'recent_projects': None,
        'project_to_edit': None
    })
from django.contrib.auth import authenticate, login

def custom_login(request):
    if request.method == "POST":
        email = request.POST['username']  # Still named 'username'
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')


# @login_required
# def search_users(request):
#     query = request.GET.get('q', '')
#     users = User.objects.filter(
#         Q(username__icontains=query) |
#         Q(first_name__icontains=query) |
#         Q(last_name__icontains=query)
#     ).exclude(id=request.user.id)
#     return render(request, 'core/search_users.html', {'users': users, 'query': query})

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(projects__category__icontains=query)  # Search by related Project category
    ).prefetch_related('projects').distinct()  # Avoid duplicate users
    for user in users:
        user.total_likes = Project.objects.filter(owner=user).aggregate(Sum('likes'))['likes__sum'] or 0
        user.total_views = Project.objects.filter(owner=user).aggregate(Sum('views'))['views__sum'] or 0
    return render(request, 'core/search_users.html', {'users': users, 'query': query})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})




@login_required
def messages_view(request):
    user = request.user
    selected_user_id = request.GET.get('user')

    # Handle sending a new message
    if request.method == "POST" and selected_user_id:
        content = request.POST.get("message")
        if content:
            receiver = get_object_or_404(PythonUser, id=selected_user_id)
            Message.objects.create(sender=user, receiver=receiver, content=content)
            return redirect(f"{request.path}?user={selected_user_id}")  # Refresh chat

    # Build conversation list
    message_users = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .values_list('sender', 'receiver')
    )
    unique_user_ids = set()
    for sender_id, receiver_id in message_users:
        other_user_id = sender_id if sender_id != user.id else receiver_id
        if other_user_id != user.id:
            unique_user_ids.add(other_user_id)

    conversation_list = []
    for other_user_id in unique_user_ids:
        other_user = PythonUser.objects.get(id=other_user_id)
        last_message = (
            Message.objects.filter(
                Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
            )
            .order_by('-timestamp')
            .first()
        )
        conversation_list.append({
            'other_user': other_user,
            'last_message': last_message.content if last_message else ''
        })

    conversation_list = sorted(conversation_list, key=lambda x: 
        Message.objects.filter(
            Q(sender=user, receiver=x['other_user']) | Q(sender=x['other_user'], receiver=user)
        ).aggregate(Max('timestamp'))['timestamp__max'], reverse=True
    )

    chat_messages = []
    selected_user = None
    if selected_user_id:
        selected_user = get_object_or_404(PythonUser, id=selected_user_id)
        chat_messages = Message.objects.filter(
            Q(sender=user, receiver=selected_user) | Q(sender=selected_user, receiver=user)
        ).order_by('timestamp')

    return render(request, 'core/messages.html', {
        'conversations': conversation_list,
        'chat_messages': chat_messages,
        'selected_user': selected_user,
    })



def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure only the owner can delete
    if request.user == project.owner:
        project.delete()
        messages.success(request, "Project deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this project.")

    return redirect('project_create') 


@login_required
def hire_now(request, user_id):
    target_user = get_object_or_404(PythonUser, id=user_id)  # user being hired

    if request.method == 'POST':
        reason_for_hire = request.POST.get('reason_for_hire')
        category = request.POST.get('category')
        budget = request.POST.get('budget')
        project_description = request.POST.get('project_description')
        personal_note = request.POST.get('personal_note')

        HiringPost.objects.create(
            user=target_user,
            reason_for_hire=reason_for_hire,
            category=category,
            budget=budget,
            project_description=project_description,
            personal_note=personal_note,
            hiring_for='Freelancing'
        )

        # Create a notification for the hired user
        Notification.objects.create(
            user=target_user,
            sender=request.user,
            message=f"{request.user.username} has sent you a hire request!"
        )


        return redirect('dashboard')  # Redirect after submit

    return render(request, 'core/hire_now.html', {'target_user': target_user})


@login_required
def send_message(request, user_id):
    receiver = get_object_or_404(PythonUser, id=user_id)  # <-- Use receiver instead of recipient
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver  # <-- Correct field name
            msg.save()
            messages.success(request, f"Message sent to {receiver.username}!")
            return redirect('search_users')
    else:
        form = MessageForm()
    return render(request, 'core/send_message.html', {'form': form, 'recipient': receiver})

# def like_project(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     project.likes += 1
#     project.save()
#     return redirect('project_view', project_id=project.id)



def like_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.likes += 1
        project.save()
        return JsonResponse({"success": True, "message": "You liked the project!"})
    return JsonResponse({"success": False, "message": "Invalid request"})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_profile(request):
    if request.method == "POST":
        user = request.user
        user.occupation = request.POST.get("occupation")
        user.company_name = request.POST.get("company_name")
        user.location = request.POST.get("location")
        user.about_me = request.POST.get("about_me")
        user.projects_descriptions = request.POST.get("projects_descriptions")
        custom_messages = request.POST.getlist('custom_message[]')
        user.custom_message = ", ".join(custom_messages)  # Save as a single string
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        user.save()
    return render(request, "core/profile.html", {"user": request.user})

from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import Message

User = get_user_model()

def compose_message(request):
    if request.method == "POST":
        recipient_username = request.POST.get('recipient')
        message_text = request.POST.get('message')
        try:
            recipient = User.objects.get(username=recipient_username)
            Message.objects.create(
                sender=request.user,
                receiver=recipient,
                content=message_text
            )
        except User.DoesNotExist:
            # Handle invalid recipient (optional)
            pass
    return redirect('messages_view')  # Replace with your messages page name
