from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import CreateView, DeleteView, ListView

from .models import Questions, SettingsBot, RelationQuestion
from .forms import SettingsBotForm, QuestionsForm, SubQuestionForm
from .utils import AuthorFilterMixin


class BotCreateView(CreateView):
    model = SettingsBot
    form_class = SettingsBotForm
    template_name = 'FAQ/create_bot.html'
    permission_clases = []

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BotCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(obj.get_absolute_url())


class SettingsBotDetail(ListView):
    paginate_by = 3
    model = Questions
    template_name = 'FAQ/detail.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Questions.objects.filter(bot=self.kwargs['bot_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bot'] = get_object_or_404(SettingsBot, id=self.kwargs['bot_id'], user=self.request.user)
        return context


class BotDeleteView(AuthorFilterMixin, DeleteView):
    model = SettingsBot
    template_name = 'FAQ/delete_bot.html'
    success_url = reverse_lazy('FAQ:bot_list')
    pk_url_kwarg = 'bot_id'


class QuestionCreateView(AuthorFilterMixin, CreateView):
    model = Questions
    form_class = QuestionsForm
    template_name = 'FAQ/create_question.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form=form, request=request)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bot'] = get_object_or_404(SettingsBot, id=self.kwargs['bot_id'], user=self.request.user)
        return context

    def form_valid(self, form, request):
        obj = form.save(commit=False)
        obj.bot_id = self.kwargs['bot_id']
        obj.save()
        if "_save" in request.POST:
            return redirect("FAQ:settings_bot_detail", bot_id=obj.bot_id)
        elif "_addanother" in request.POST:
            redirect_url = request.path
            return redirect(redirect_url)
        elif "_add_sub" in request.POST:
            return redirect(obj.get_absolute_url())


class QuestionDeleteView(DeleteView):
    model = Questions
    template_name = 'FAQ/delete_question.html'
    slug_url_kwarg = 'bot_id'
    pk_url_kwarg = 'question_id'

    def get_success_url(self, **kwargs):
        return reverse_lazy("FAQ:settings_bot_detail", kwargs={'bot_id': self.object.bot_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bot_id'] = self.kwargs['bot_id']
        context['question_id'] = self.kwargs['question_id']
        return context


@login_required
def edit_question(request, bot_id, question_id):
    bot = get_object_or_404(SettingsBot, id=bot_id, user=request.user)
    question = get_object_or_404(Questions, id=question_id, bot=bot_id)
    QuestionInlineFormSet = inlineformset_factory(Questions, RelationQuestion, fk_name='base', form=SubQuestionForm, can_delete=True)
    if request.method == "POST":
        form = QuestionsForm(data=request.POST, instance=question)
        formset = QuestionInlineFormSet(request.POST, request.FILES, form_kwargs={'bot_id': bot_id}, instance=question)
        print(formset)
        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save()
            if "_save" in request.POST:
                return redirect("FAQ:settings_bot_detail", bot_id=bot.pk)
            elif "_addanother" in request.POST:
                return redirect("FAQ:create_question", bot_id=bot.pk)
            elif "_continue" in request.POST:
                redirect_url = request.path
                return redirect(redirect_url)
    else:
        form = QuestionsForm(instance=question)
        formset = QuestionInlineFormSet(form_kwargs={'bot_id': bot_id}, instance=question)
    return render(request, 'FAQ/edit_questions.html', {'question': question,
                                                       'bot': bot,
                                                       'form': form,
                                                       'formset': formset})


@login_required
def bot_list(request):
    bots = SettingsBot.objects.filter(user=request.user)
    return render(request, 'FAQ/list.html', {'section': 'My bots',
                                             'bots': bots,
                                             })


# @login_required
# def settings_bot_detail(request, bot_id):
#     bot = get_object_or_404(SettingsBot, id=bot_id, user=request.user)
#     questions = Questions.objects.filter(bot=bot_id)
#     return render(request,'FAQ/detail.html', {'bot': bot,
#                                               'questions': questions})


@login_required
def edit_settings_bot(request, bot_id):
    bot = get_object_or_404(SettingsBot, id=bot_id, user=request.user)
    if request.method == 'POST':
        form = SettingsBotForm(data=request.POST, instance=bot)
        if form.is_valid():
            if form.is_valid():
                form.save()
                return redirect(bot.get_absolute_url())
    else:
        form = SettingsBotForm(instance=bot)
    return render(request, 'FAQ/bot_settings/settings.html', {'bot': bot,
                                                              'form': form})
