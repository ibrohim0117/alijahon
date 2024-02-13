from celery import shared_task
from django.core.mail import send_mail


@shared_task
def task_send_mail(email):
    subject = 'test'
    message = 'test'
    from_email = 'ibrohim.dev.uz@gmail.com'
    recipient_list = [email]
    html_message = 'success_login.html'

    return send_mail(subject, message, from_email, recipient_list, html_message=html_message)
