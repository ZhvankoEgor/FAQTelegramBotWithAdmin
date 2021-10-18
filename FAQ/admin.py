from subprocess import Popen
import psutil
from django.contrib import admin
from .models import questions, relation_question


# Рестарт бота реализован через стандартные Action, чтобы не менять шаблон панели администратора и упростить поддержку
@admin.action(description='Перезапустить бота и обновить вопросы')
def run_bot(modeladmin, request, queryset):
    process_command = ['python3', 'manage.py', 'app']
    for process in psutil.process_iter():
        if process.cmdline() == process_command:
            print('Process found. Terminating it.')
            process.terminate()
            break
    print('Process not found: starting it.')
    Popen(process_command)


# Добавляем возможность добавлять дочерние вопросы в одной форме, согласно ТЗ
class RelationQuestionInline(admin.TabularInline):
    model = relation_question
    fk_name = "base"

# Форма для редактирования записей
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'general')
    inlines = (RelationQuestionInline,)
    actions = [run_bot]

admin.site.register(questions, QuestionsAdmin)
