from django.db import models
from django.utils.safestring import mark_safe

# Таблица для хранения вопросов
class questions(models.Model):
    question = models.CharField(max_length=30, verbose_name="Вопрос")
    answer = models.TextField(default="No text", verbose_name="Ответ на вопрос")
    id = models.BigAutoField(primary_key=True)
    general = models.BooleanField(default=False, verbose_name="Отображать на стартовой странице")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменен")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ('-id',)

    def button(self, obj):
        return mark_safe(f'<a class="button" >Кнопка</a>')

    def __str__(self):
        return self.question

    def data(self):
        return [self.question, self.answer, self.id, self.general]

# Таблица для хранения связей вопросов
class relation_question(models.Model):
    base = models.ForeignKey("questions", related_name='Основной_вопрос', on_delete=models.CASCADE, verbose_name="Основной вопрос")
    sub = models.ForeignKey("questions", related_name='Дополнительный_вопрос', on_delete=models.CASCADE, verbose_name="Дополнительный вопрос")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Изменен")

    class Meta:
        verbose_name = "Таблица связей вопросов"
        verbose_name_plural = "Таблица связей вопросов"