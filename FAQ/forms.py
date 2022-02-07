from django import forms
from django.forms import ModelForm, PasswordInput, inlineformset_factory, BaseInlineFormSet
from .models import SettingsBot, RelationQuestion, Questions
from django.forms import BaseModelFormSet


class SubQuestionForm(forms.ModelForm):
    """Показывает вопросы выбранного бота"""
    def __init__(self, *args, **kwargs):
        self.bot_id = kwargs.pop('bot_id', None)
        super(SubQuestionForm, self).__init__(*args, **kwargs)
        self.fields['sub'] = forms.ModelChoiceField(Questions.objects.filter(bot=self.bot_id))

    class Meta:
        model = RelationQuestion
        fields = ['sub']


class QuestionsForm(ModelForm):

    class Meta:
        model = Questions
        exclude = ['bot']


class SettingsBotForm(ModelForm):
    token = forms.CharField(widget=PasswordInput(render_value=True))

    class Meta:
        model = SettingsBot
        exclude = ['user',
                   'status',]



