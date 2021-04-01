from users.models import Account
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import redirect
from asgiref.sync import sync_to_async
from .models import WorkGroup, WorkGroupUser, Chat
import json

# get user object
@sync_to_async
def getUsrObj(user):
    bool1 = Account.objects.filter(email=user).exists()
    if bool1:
        return Account.objects.get(email=user)
    return False

# get group object
@sync_to_async
def getGrpObj(group_ID):
    bool1 = WorkGroup.objects.filter(groupID=group_ID).exists()
    if bool1:
        return WorkGroup.objects.get(groupID=group_ID)
    return False

# save chat details such as user, group, message
@sync_to_async
def saveChat(user, workGroup, message):
    chat = Chat()
    chat.author = user
    chat.work_group = workGroup
    chat.message = message
    chat.save()

# handles the asynchronous channels using web sockets
class ChatRoomConsumer(AsyncWebsocketConsumer):
    # connects to the chat
    async def connect(self):
        self.groupID = self.scope["url_route"]["kwargs"]["groupID"]
        self.email = self.scope["user"]
        print(self.email)

        self.userObj = await getUsrObj(self.email)
        self.groupObj = await getGrpObj(self.groupID)

        self.room_group_name = f"chat{self.groupID}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # disconnects from the chat
    async def disconnect(self, close_code):
        if "room_group_name" in dir(self):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # receives the chat 
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        email = text_data_json["user"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": email
            }
        )
        
    # saves the chat message content
    # Function name is same as type above
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        await saveChat(self.userObj, self.groupObj, message)

        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
        }))
    pass
