from django.db import models


class Pose(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    file = models.FileField()

    def __str__(self):
        return self.name


class PoseAnalysis(models.Model):
    pose = models.ForeignKey("pose_analyser.Pose", blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField()
    analysis = models.TextField(blank=True, null=True)
