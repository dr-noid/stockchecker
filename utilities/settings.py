from utilities.json_parser import parse_json


class _Settings:
    db_reset: bool
    notifications: bool
    whatsapp_group_id: str

    def __init__(self, db_reset=True, notifications=False):
        self.db_reset = db_reset
        self.notifications = notifications
        self.whatsapp_group_id = str(parse_json("config/env.json"))


program_settings = _Settings()

if __name__ == '__main__':
    pass
