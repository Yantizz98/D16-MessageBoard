from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Advert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY = (
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('gild_masters', 'Гилдмастеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'))
    category = models.CharField(max_length=16, choices=CATEGORY, verbose_name='Категория', default='tanks')
    createDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name='Название')
    text = models.TextField()
    upload = models.FileField(upload_to='uploads/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)