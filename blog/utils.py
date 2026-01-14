from django.core.mail import send_mail
from django.conf import settings


def send_test_email(user_email, username):
    """Отправка тестового письма."""
    subject = 'Добро пожаловать в Blogicum!'
    message = f'''
    Приветствуем вас, {username}!

    Спасибо за регистрацию на нашем сайте Blogicum.

    С уважением,
    Команда Blogicum
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return True
