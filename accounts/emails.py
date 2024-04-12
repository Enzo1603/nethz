from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings


def send_verification_email(user, request):
    def _send_email():
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)

        mail_subject = "Activate your account."
        message = render_to_string(
            "accounts/verification_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": uid,
                "token": token,
            },
        )
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    Thread(target=_send_email).start()
