from django.urls import re_path

from pose_analyser import consumers

websocket_urlpatterns = [
    re_path(r'ws/poses/(?P<pose_id>\w+)/$', consumers.PoseConsumer.as_asgi()),
]