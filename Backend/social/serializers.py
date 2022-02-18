from django.urls import path, include
from social import models
from rest_framework import routers, serializers, viewsets
from accounts.serializers import UserListSerializer


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    user_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Post
        fields = "__all__"

    @staticmethod
    def get_user_detail(obj):
        serializer = UserListSerializer(obj.user, many=False)
        return serializer.data

    @staticmethod
    def get_likes(obj):
        reacts = models.PostLike.objects.filter(post=obj).count()
        return reacts

    @staticmethod
    def get_comments(obj):
        comments = models.PostComment.objects.filter(post=obj)
        data = PostCommentSerializer(comments, many=True).data
        return data


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.PostLike
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.PostComment
        fields = "__all__"

    @staticmethod
    def get_replies(obj):
        replies = models.PostCommentReply.objects.filter(comment = obj)
        data = PostCommentReplySerializer(replies, many=True).data
        return data


class PostCommentReplySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.PostCommentReply
        fields = "__all__"
