from django import forms

from .models import *


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ('category', 'title', 'text', 'upload')

    def __init__(self, *args, **kwargs):
        super(AdvertForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок"
        self.fields['text'].label = "Текст объявления:"
        self.fields['upload'].label = "Файл:"


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"


class ResponsesFilterForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ResponsesFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Объявление',
            queryset=Advert.objects.filter(author_id=user.id).order_by('-createDate').values_list('title', flat=True),
            empty_label="Все",
            required=False
        )

