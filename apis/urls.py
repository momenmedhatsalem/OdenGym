from django.urls import path
from .views import UserAPIView


urlpatterns = [
    path("users/<int:pk>/", UserAPIView.as_view(), name="current_user"),
    

]
