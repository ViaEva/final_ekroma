from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.generics import (
#     ListAPIView,
#     RetrieveAPIView,
#     DestroyAPIView, 
#     UpdateAPIView, 
#     CreateAPIView)

from .models import (
    Post,
    Tag,
    Comment,
    Rating
)
from .serializers import (
    PostListSerializer,
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    RatingSerializer,
    TagSerializer,
    LikeSerializer
)
from .permissions import IsOwner

# class PostListView(ListAPIView):
#     # queryset = Post.objects.filter(status='open')
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set-rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk # TODO
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            post=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response('ZAGLUSHKA') # TODO: fix

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        post = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'post': post
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')


class CommentCreateDeleteView(
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()




"""  
actions

create() - POST
retrieve() - GET /post/1/
list() - GET /post/
destroy() - DELETE /post/1/
partial_update() - PATCH /post/1/
update() - PUT /post/1/
"""

# TODO: fix rating
# TODO: фильтрация, поиск, пагинация
# TODO: кастомизация админ-панели
