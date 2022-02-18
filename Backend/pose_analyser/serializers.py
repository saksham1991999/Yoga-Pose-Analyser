from rest_framework.serializers import ModelSerializer, ReadOnlyField

from pose_analyser.models import Pose, PoseAnalysis


class PoseSerializer(ModelSerializer):
    class Meta:
        model = Pose
        fields = "__all__"


class AnalysisSerializer(ModelSerializer):
    analysis = ReadOnlyField()
    output = ReadOnlyField()

    class Meta:
        model = PoseAnalysis
        fields = "__all__"
