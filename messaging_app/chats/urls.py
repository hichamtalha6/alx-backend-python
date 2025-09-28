# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin

# Create the router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),   # ✅ include DRF router
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),   # ✅ mount chats API under /api/
    
]





