import telebot
import constants

import sys

from telegram import MessageEntity, TelegramObject, Animation, PhotoSize


class Game(TelegramObject):


    def __init__(self,
                 title,
                 description,
                 photo,
                 text=None,
                 text_entities=None,
                 animation=None,
                 **kwargs):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities or list()
        self.animation = animation

    @classmethod
    def de_json(cls, data, bot):
        if not data:
            return None

        data = super(Game, cls).de_json(data, bot)

        data['photo'] = PhotoSize.de_list(data.get('photo'), bot)
        data['text_entities'] = MessageEntity.de_list(data.get('text_entities'), bot)
        data['animation'] = Animation.de_json(data.get('animation'), bot)

        return cls(**data)

    def to_dict(self):
        data = super(Game, self).to_dict()

        data['photo'] = [p.to_dict() for p in self.photo]
        if self.text_entities:
            data['text_entities'] = [x.to_dict() for x in self.text_entities]

        return data

    def parse_text_entity(self, entity):

        if sys.maxunicode == 0xffff:
            return self.text[entity.offset:entity.offset + entity.length]
        else:
            entity_text = self.text.encode('utf-16-le')
            entity_text = entity_text[entity.offset * 2:(entity.offset + entity.length) * 2]

        return entity_text.decode('utf-16-le')

    def rules(bot, update):

        if update.message.chat.username == ONTOPIC_USERNAME:
            update.message.reply_text(ONTOPIC_RULES, parse_mode=ParseMode.HTML,
                                      disable_web_page_preview=True, quote=False)
            update.message.delete()
        elif update.message.chat.username == OFFTOPIC_USERNAME:
            update.message.reply_text(OFFTOPIC_RULES, parse_mode=ParseMode.HTML,
                                      disable_web_page_preview=True, quote=False)
            update.message.delete()
        else:
            update.message.reply_text("Hmm. You're not in a python-telegram-bot group, "
                                      "and I don't know the rules around here.")

    def parse_text_entities(self, types=None):

        if types is None:
            types = MessageEntity.ALL_TYPES

        return {
            entity: self.parse_text_entity(entity)
            for entity in self.text_entities if entity.type in types
        }