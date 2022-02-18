from rest_framework.viewsets import generics

from .serializers import UserSerializer
from .models import User


class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer = UserSerializer
