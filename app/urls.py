from app.views import UserViewSet, ChatViewSet, ChatRoomViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

route = DefaultRouter()
route.register(r'users', UserViewSet)
route.register(r'chat_room', ChatRoomViewSet)
route.register(r'chat', ChatViewSet)


urlpatterns = [
    path('', include(route.urls)),
    path('login/', TokenObtainPairView.as_view())
]