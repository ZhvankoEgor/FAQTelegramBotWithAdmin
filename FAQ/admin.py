import os
import sys
from django.contrib import admin
from .models import questions, relation_question
from django.utils.safestring import mark_safe


@admin.action(description='Перезапустить бота и обновить вопросы')
def run_bot(modeladmin, request, queryset):
    os.system("python3 manage.py app")
    # os.execv(sys.executable, [sys.executable, "/media/sf_Projects/FAQ_DB_project/app.py"] + sys.argv)

class RelationQuestionInline(admin.TabularInline):
    model = relation_question
    fk_name = "base"


class questionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'general', 'button')
    inlines = (RelationQuestionInline,)
    actions = [run_bot]

    def button(self, obj):
        return mark_safe(f'<a class="button" >Кнопка</a>')

    # def run_bot(self):
    #     return os.system("python3 manage.py app")



admin.site.register(questions,questionsAdmin)
# Register your models here.


# class MembershipInline(admin.TabularInline):
#     model = Membership
#     extra = 1
#
# class PersonAdmin(admin.ModelAdmin):
#     inlines = (MembershipInline,)
#
# class GroupAdmin(admin.ModelAdmin):
#     inlines = (MembershipInline,)
# admin.site.register(Person, PersonAdmin)
# admin.site.register(Group, GroupAdmin)