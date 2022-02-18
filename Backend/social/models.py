from django.db import models


class Follower(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "follower")


class Post(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    video = models.FileField()


class PostLike(models.Model):
    post = models.ForeignKey('social.Post', on_delete = models.CASCADE )
    user = models.ForeignKey('accounts.User', on_delete = models.CASCADE )
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Post Reacts"
        unique_together = ['post', 'user']


class PostComment(models.Model):
    post = models.ForeignKey('social.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    comment = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)


class PostCommentReply(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,related_name="user_reply")
    comment = models.ForeignKey('social.PostComment', on_delete = models.CASCADE)
    reply = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Post Comment Replies"