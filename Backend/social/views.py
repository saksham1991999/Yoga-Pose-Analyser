from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.db.models import Q

from social import models, serializers
from social.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        following_id = models.Follower.objects.filter(follower=self.request.user).values_list("user", flat=True)
        query_set = models.Post.objects.filter(user__id__in=following_id)
        if not query_set.exists():
            query_set = models.Post.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            query_set = query_set.filter(description__icontains=search)

        order_by = self.request.query_params.get('orderby', None)
        if order_by:
            if order_by == "recent":
                query_set = query_set.orderby('-date')
        return query_set


class PostReactViewSet(viewsets.ModelViewSet):
    queryset = models.PostLike.objects.all()
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = models.PostComment.objects.all()
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostCommentReplyViewSet(viewsets.ModelViewSet):
    queryset = models.PostCommentReply.objects.all()
    serializer_class = serializers.PostCommentReplySerializer
    permission_classes = [IsOwnerOrReadOnly]
