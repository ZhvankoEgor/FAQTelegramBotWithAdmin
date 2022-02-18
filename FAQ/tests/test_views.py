from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from FAQ.views import *
from FAQ.urls import *


class ViewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test_user1")
        self.user2 = User.objects.create(username="test_user2")

        self.bot1 = SettingsBot.objects.create(bot_name="bot1",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe1")
        self.bot2 = SettingsBot.objects.create(bot_name="bot2",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe2")
        self.bot3 = SettingsBot.objects.create(bot_name="bot3",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe3")
        self.bot4 = SettingsBot.objects.create(bot_name="bot4",
                                               user=self.user2,
                                               token="qweqweqweqweqweqweqwe4")
        self.bot5 = SettingsBot.objects.create(bot_name="bot5",
                                               user=self.user2,
                                               token="qweqweqweqweqweqweqwe5")

        self.question1 = Questions.objects.create(question="question1",
                                                  answer="answer1",
                                                  bot=self.bot2)
        self.question2 = Questions.objects.create(question="question2",
                                                  answer="answer2",
                                                  bot=self.bot2)
        self.question3 = Questions.objects.create(question="question3",
                                                  answer="answer3",
                                                  bot=self.bot2)
        self.question4 = Questions.objects.create(question="question4",
                                                  answer="answer4",
                                                  bot=self.bot2)
        self.question5 = Questions.objects.create(question="question5",
                                                  answer="answer5",
                                                  bot=self.bot1)
        self.question6 = Questions.objects.create(question="question6",
                                                  answer="answer6",
                                                  bot=self.bot1)
        self.question7 = Questions.objects.create(question="question7",
                                                  answer="answer7",
                                                  bot=self.bot1)
        self.question8 = Questions.objects.create(question="question8",
                                                  answer="answer8",
                                                  bot=self.bot1)

    def test_bot_list(self):
        self.client.force_login(self.user1)
        url = reverse("FAQ:bot_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['bots']),
                         '<QuerySet [<SettingsBot: bot3>, <SettingsBot: bot2>, <SettingsBot: bot1>]>')

    def test_create_bot(self):
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        self.client.force_login(self.user1)
        url = reverse("FAQ:create_bot")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bot_name': 'bot6',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe6'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(SettingsBot.objects.all().count(), 6)
        bot = get_object_or_404(SettingsBot, token=data['token'], user=self.user1)
        self.assertEqual(bot.bot_name, 'bot6')

    def test_edit_settings_bot(self):
        self.client.force_login(self.user1)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:edit_settings_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bot_name': 'bot2',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe23'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        bot_updated = get_object_or_404(SettingsBot, token=data['token'], user=self.user1)
        self.assertEqual(bot.pk, bot_updated.pk)

    def test_edit_settings_bot_another_user(self):
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:edit_settings_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login/?next=/FAQ/18/settings/")
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        data = {'bot_name': 'bot2',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe23'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 404)
        bot_updated = str(SettingsBot.objects.filter(token=data['token']))
        self.assertEqual(bot_updated, "<QuerySet []>")

    def test_delete_bot(self):
        self.client.force_login(self.user1)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe3', user=self.user1)
        url = reverse("FAQ:delete_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(SettingsBot.objects.all().count(), 4)
        bot_deleted = str(SettingsBot.objects.filter(token='qweqweqweqweqweqweqwe3'))
        self.assertEqual(bot_deleted, "<QuerySet []>")

    def test_delete_bot_another_user(self):
        self.client.force_login(self.user2)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe3', user=self.user1)
        url = reverse("FAQ:delete_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot_deleted = str(SettingsBot.objects.filter(token='qweqweqweqweqweqweqwe3'))
        self.assertEqual(bot_deleted, "<QuerySet [<SettingsBot: bot3>]>")

    def test_question_list(self):
        self.client.force_login(self.user1)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:settings_bot_detail", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        questions = str(response.context['questions'])
        self.assertEqual(questions, "<QuerySet [<Questions: question4>, <Questions: question3>, <Questions: question2>, <Questions: question1>]>")
