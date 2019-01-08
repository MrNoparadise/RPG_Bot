from telegram import TelegramObject, User


class GameHighScore(TelegramObject):


    def __init__(self, position, user, score):
        self.position = position
        self.user = user
        self.score = score

    @classmethod
    def de_json(cls, data, bot):
        if not data:
            return None

        data = super(GameHighScore, cls).de_json(data, bot)

        data['user'] = User.de_json(data.get('user'), bot)

        return cls(**data)