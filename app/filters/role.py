from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message
from models.jaynecobbdatabase import UsersToChats, Roles


class RoleFilter(BaseFilter):
    owner_role_id = Roles.get(name='owner').role_id
    
    def __init__(self, role: Union[int, str]):
        
        if isinstance(role, str):
            self.role = Roles.get(Roles.name == role).role_id
        else:
            self.role = role

    async def __call__(self, message: Message) -> bool: 
        if(self.role == self.owner_role_id):
            return bool(
                UsersToChats.select().where(
                (UsersToChats.user == message.from_user.id) 
                & (UsersToChats.role == self.role) 
            ).count())
            
            
        return bool(
            UsersToChats.select().where(
                (UsersToChats.user == message.from_user.id) 
                & (UsersToChats.role == self.role) 
                & (UsersToChats.chat == message.chat.id)
            ).count()
        )