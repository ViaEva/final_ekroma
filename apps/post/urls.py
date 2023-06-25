from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentCreateDeleteView, TagViewSet


router = DefaultRouter()
router.register('post', PostViewSet, 'post')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('tags', TagViewSet, 'tags')
urlpatterns = [
    
]
urlpatterns += router.urls
