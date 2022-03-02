import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from accounts.models import User
from pose_analyser.models import Pose
from pose_analyser.pose_base64 import imgkeypoints


class PoseConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connection request received")
        self.pose_id = self.scope['url_route']['kwargs']['pose_id']
        self.pose = await get_pose(self.pose_id)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        pass

    # Receive message from WebSocket
    async def receive_json(self, text_data):
        self.image = text_data.get('image', None)
        if self.image:
            self.image = self.image.replace("data:image/png;base64,", "").strip()
            im_b64, analysis = imgkeypoints(self.pose.name, str(self.image))
            data = {
                'image': im_b64,
                'analysis': analysis
            }
            # print(analysis)
            # print(self.image)
            await self.send_json(data)

    async def send_to_websocket(self, event):
        await self.send_json(event)


@database_sync_to_async
def get_pose(pose_id):
    pose = Pose.objects.get(id=pose_id)
    return pose
