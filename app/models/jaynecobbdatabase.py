from peewee import *

database = PostgresqlDatabase('jaynecobbdatabase', **{'host': '192.168.0.9', 'port': 5432, 'user': 'cobb', 'password': 'cobbpass'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Chats(BaseModel):
    anti_caps = BooleanField(constraints=[SQL("DEFAULT false")])
    anti_stickers_spam = BooleanField(constraints=[SQL("DEFAULT false")])
    antibot = BooleanField()
    antibot_text = CharField(null=True)
    chat_id = IntegerField(primary_key=True)
    chat_link = CharField(null=True)
    chat_title = CharField()
    link_command_name = CharField(null=True)
    log_text = BooleanField(constraints=[SQL("DEFAULT true")])
    remove_voices = BooleanField(constraints=[SQL("DEFAULT false")])
    rules_text = CharField(null=True)
    welcome_set = BooleanField(constraints=[SQL("DEFAULT false")])
    welcome_text = CharField(null=True)

    class Meta:
        table_name = 'chats'

class Roles(BaseModel):
    description = CharField(null=True)
    name = CharField()
    role_id = AutoField()

    class Meta:
        table_name = 'roles'

class Users(BaseModel):
    custom_title = CharField(null=True)
    first_join = DateTimeField()
    role = ForeignKeyField(column_name='role_id', constraints=[SQL("DEFAULT 0")], field='role_id', model=Roles)
    user_id = IntegerField(primary_key=True)
    warn_count = SmallIntegerField()

    class Meta:
        table_name = 'users'

class Quotes(BaseModel):
    chat = ForeignKeyField(column_name='chat_id', field='chat_id', model=Chats)
    create_time = DateTimeField()
    quote_id = AutoField()
    submitter = ForeignKeyField(column_name='submitter_id', field='user_id', model=Users)
    submitter_name = CharField()
    text = CharField()

    class Meta:
        table_name = 'quotes'

class UsersToChats(BaseModel):
    chat = ForeignKeyField(column_name='chat_id', field='chat_id', model=Chats)
    is_banned = BooleanField()
    user = ForeignKeyField(column_name='user_id', field='user_id', model=Users)

    class Meta:
        table_name = 'users_to_chats'
        indexes = (
            (('user', 'chat'), True),
        )
        primary_key = CompositeKey('chat', 'user')

class UsersToQuotes(BaseModel):
    quote = ForeignKeyField(column_name='quote_id', constraints=[SQL("DEFAULT nextval('users_to_quotes_quote_id_seq'::regclass)")], field='quote_id', model=Quotes)
    user = ForeignKeyField(column_name='user_id', field='user_id', model=Users)

    class Meta:
        table_name = 'users_to_quotes'
        indexes = (
            (('user', 'quote'), True),
        )
        primary_key = CompositeKey('quote', 'user')

