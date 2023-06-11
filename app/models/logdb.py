from peewee import *

database = PostgresqlDatabase('logdb', **{'host': '192.168.0.9', 'port': 5432, 'user': 'cobb', 'password': 'cobbpass'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Newtable(BaseModel):
    chat_id = IntegerField()
    chat_title = CharField(null=True)
    chat_username = CharField(null=True)
    forward_date = DateTimeField(null=True)
    forward_from_chat_id = IntegerField(null=True)
    forward_from_chat_title = CharField(null=True)
    forward_from_chat_username = CharField(null=True)
    forward_from_user_id = IntegerField(null=True)
    forward_from_user_username = CharField(null=True)
    forward_user_first_name = CharField(null=True)
    from_user_first_name = CharField(null=True)
    from_user_id = IntegerField(null=True)
    from_user_is_bot = BooleanField(null=True)
    from_user_last_name = CharField(null=True)
    from_user_username = CharField(null=True)
    message_date = DateTimeField()
    message_edit_date = IntegerField(null=True)
    message_id = IntegerField()
    message_text = CharField()
    mod_command = CharField(null=True)
    reply_to_message_from_username = CharField(null=True)
    reply_to_message_id = IntegerField(null=True)
    reply_to_message_text = CharField(null=True)

    class Meta:
        table_name = 'newtable'
        indexes = (
            (('chat_id', 'message_id'), True),
        )
        primary_key = CompositeKey('chat_id', 'message_id')

