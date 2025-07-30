from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        notifications_count = recent_notifications.count()
        return {
            'recent_notifications': recent_notifications,
            'notifications_count': notifications_count
        }
    return {}
