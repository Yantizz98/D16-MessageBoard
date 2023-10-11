from datetime import timezone, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Response, Advert


@shared_task
def respond_send_email(respond_id):
    respond = Response.objects.get(id=respond_id)
    send_mail(
        subject=f'Доска объявлений MMORPG: новый отклик на объявление!',
        message=f'Доброго дня, {respond.advert.author}, ! На ваше объявление есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/responses/{respond.advert.id}',
        from_email='',
        recipient_list=[respond.advert.author.email, ],
    )

@shared_task
def respond_accept_send_email(response_id):
    respond = Response.objects.get(id=response_id)
    print(respond.advert.author.email)
    send_mail(
        subject=f'Доска объявлений MMORPG: Ваш отклик принят!',
        message=f'Доброго дня, {respond.author}, Автор объявления {respond.advert.title} принял Ваш отклик!\n'
                f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/responses',
        from_email='Yantizz@yandex.com',
        recipient_list=[respond.advert.author.email, ],
    )

@shared_task
def send_mail_monday_8am():
    now = timezone.now()
    list_week_adverts = list(Advert.objects.filter(createDate__gte=now - timedelta(days=7)))
    if list_week_adverts:
        for user in User.objects.filter():
            print(user)
            list_adverts = ''
            for advert in list_week_adverts:
                list_adverts += f'\n{advert.title}\nhttp://127.0.0.1:8000/advert/{advert.id}'
            send_mail(
                subject=f'Доска объявлений MMORPG: объявления за прошедшую неделю.',
                message=f'Доброго дня, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, '
                        f'появившимися за последние 7 дней:\n{list_adverts}',
                from_email='',
                recipient_list=[user.email, ],
            )

