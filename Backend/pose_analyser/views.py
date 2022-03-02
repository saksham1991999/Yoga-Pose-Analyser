import os

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from pose_analyser.models import Pose, PoseAnalysis
from pose_analyser.serializers import PoseSerializer, AnalysisSerializer

from pose_analyser.pose import imgkeypoints


class PoseViewSet(viewsets.ModelViewSet):
    queryset = Pose.objects.all()
    serializer_class = PoseSerializer

    @action(detail=True, methods=['post'], name="analyse", serializer_class=AnalysisSerializer)
    def analyse(self, request, pk=None):
        pose = self.get_object()
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cwd = os.getcwd()
            pose_analysis = PoseAnalysis.objects.get(id=serializer.data["id"])
            # image_url = serializer.validated_data["image"]
            image_url = pose_analysis.image.url
            image_dir = os.path.join(cwd, image_url[1:])
            analysis = imgkeypoints("goddess", image_dir)
            pose_analysis.analysis = analysis
            pose_analysis.save()
            serializer = AnalysisSerializer(pose_analysis, many=False)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def HomeView(request):
    context = {}
    return render(request, 'index.html', context)


def AnalysisView(request, id):
    pose = Pose.objects.get(id=id)
    context = {"pose": pose}
    return render(request, 'analysis.html', context)