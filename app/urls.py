from app.views import UserViewSet, ChatViewSet, ChatRoomViewSet
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register(r'users', UserViewSet)
route.register(r'chat_room', ChatRoomViewSet)
route.register(r'chat', ChatViewSet)


urlpatterns = [
    path('', include(route.urls)),
    path('login/', obtain_auth_token)
]