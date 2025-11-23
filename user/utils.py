from alumni.models import Alumniuser


def c_user_alumni(user):
	objects = Alumniuser.objects.get(user=user)
	alumni = ""
	if objects:
		alumni = objects.alumni
	return alumni


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.crypto import get_random_string


def generate_token():
	return get_random_string(length=32)

def send_password_reset_email(user, token):
	user_id_str = str(user.user_profile.id)
	uidb64 = urlsafe_base64_encode(user_id_str.encode())
	print("uidb64:=======================",uidb64)
	reset_link = f"{settings.BASE_URL}/users/password-reset/confirm/{uidb64}/{token}/"

	subject = 'SIG-Alumni Account - Password Reset Request'
	email_body = render_to_string('emailtemplates/password_reset_email.html', {'reset_link': reset_link, 'user': user})
	sender_email = settings.EMAIL_HOST_USER
	recipient_email = user.email

	email = EmailMessage(subject, email_body, sender_email, [recipient_email])
	email.content_subtype = 'html'
	email.send()

def send_activate_user_email(user, token):
	user_id_str = str(user.user_profile.id)
	uidb64 = urlsafe_base64_encode(user_id_str.encode())
	print("uidb64:=======================",uidb64)
	activate_link = f"{settings.BASE_URL}/users/user-activate/confirm/{uidb64}/{token}/"

	subject = 'SIG-Alumni Account - Activate Member Account'
	email_body = render_to_string('emailtemplates/activate_user_email.html', {'activate_link': activate_link, 'user': user})
	sender_email = settings.EMAIL_HOST_USER
	recipient_email = user.email

	email = EmailMessage(subject, email_body, sender_email, [recipient_email])
	email.content_subtype = 'html'
	email.send()