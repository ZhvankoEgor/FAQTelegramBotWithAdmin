from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..views import *
from ..urls import *


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

    def test_bot_list(self):
        self.client.force_login(self.user1)
        url = reverse("FAQ:bot_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['bots']),
                         '<QuerySet [<SettingsBot: 1>, <SettingsBot: 2>, <SettingsBot: 3>]>')

    def test_create_bot(self):
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        self.client.force_login(self.user1)
        url = reverse("FAQ:create_bot")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bot_name': 'bot6',
                'status': 'включен',
                # 'user': self.user1,
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe6'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(SettingsBot.objects.all().count(), 6)
        self.assertEqual(get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe6', user=self.user1).bot_name, 'bot6')
