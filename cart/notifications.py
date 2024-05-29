# from django.contrib.auth import get_user_model  # Assuming User model is in contrib.auth
# from django_notifications import notify

# def SendNotification(message, recipient_username):
#     try:
#         user = get_user_model().objects.get(username=recipient_username)
#         notify.send(user, recipient=user, verb='Notification message:', description=message)
#     except get_user_model().DoesNotExist:
#         print(f"User with username '{recipient_username}' not found.")
