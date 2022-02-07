from FAQ.management.commands._loader import db


class Settings:
    """Настройки телеграм бота"""

    def __init__(self):

        self.settings_datas = db.settings_bot()
        self.title_text = self.settings_datas[0][0]
        self.interval_refresh_base = self.settings_datas[0][1]
        self.title_button_row = self.settings_datas[0][2]
        self.other_button_row = self.settings_datas[0][3]