from django.urls import re_path
from . import consumers

# routes the chats to the approriate path using websockets
websocket_urlpatterns = [
    re_path(r'ws/group/(?P<groupID>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/$',
            consumers.ChatRoomConsumer.as_asgi()),
]
