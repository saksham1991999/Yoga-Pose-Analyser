from django.contrib import admin
import nested_admin

from . import models


class ReactInlineAdmin(nested_admin.NestedTabularInline):
    model = models.PostLike
    extra = 0


class CommentReplyInlineAdmin(nested_admin.NestedTabularInline):
    model = models.PostCommentReply
    extra = 1


class CommentInlineAdmin(nested_admin.NestedTabularInline):
    model = models.PostComment
    inlines = [CommentReplyInlineAdmin]
    extra = 0


class PostAdmin(nested_admin.NestedModelAdmin):
    inlines = [CommentInlineAdmin, ReactInlineAdmin ]
    list_display = ['id', 'user', 'description', 'timestamp']
    list_display_links = ['id', 'user', 'description', 'timestamp']
    search_fields = ['description']


class FollowerAdmin(nested_admin.NestedModelAdmin):
    list_display = ['id', 'user', 'follower', 'created_at']
    list_display_links = ['id', 'user', 'follower', 'created_at']
    search_fields = ['user', 'follower']


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Follower, FollowerAdmin)
