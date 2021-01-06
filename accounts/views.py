from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail


def send_login_email(request):
    """
    представление отправления почты
    при регистрации
    """
    email = request.POST['email']

    send_mail(
        'Your login link for Superlists',
        'body tbc',
        'noreply@superlists',
        [email]
    )
    return redirect('/')
