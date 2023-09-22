from peewee import *
import datetime

db = SqliteDatabase('db/conversations.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)


class Conversation(BaseModel):
    user = ForeignKeyField(User, backref='conversations', unique=True)
    chat_id = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


def initialize_orm():
    db.connect()
    db.create_tables([User, Conversation])


def create_conversation_for_user(param_username, param_chat_id):
    user, user_created = User.get_or_create(username=param_username)

    conversation, conversation_created = (
        Conversation.create(user_id=user.id, chat_id=param_chat_id)
    )

    return conversation


def get_conversation_id_for_user(param_username):
    user, user_created = User.get_or_create(username=param_username)

    try:
        conversation = Conversation.get(user_id=user.id)
        return conversation.chat_id
    except:
        return False


def update_conversation_id_for_user(param_username, param_chat_id):
    user, user_created = User.get_or_create(username=param_username)

    conversation = Conversation.get(user_id=user.id)
    conversation.chat_id = param_chat_id
    conversation.save()

    return conversation
