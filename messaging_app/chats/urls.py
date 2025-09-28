# messaging_app/chats/urls.py
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create the router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Expose router URLs
urlpatterns = router.urls
