from rest_framework import generics

from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class UserAPIView(generics.RetrieveUpdateAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer