class _Settings:
    db_reset: bool
    notifications: bool

    def __init__(self, db_reset=True, notifications=True):
        self.db_reset = db_reset
        self.notifications = notifications


program_settings = _Settings()

if __name__ == '__main__':
    pass
