from django.urls import path
from . import views

app_name = 'pose_analyser'

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('poses/<int:id>/', views.AnalysisView, name='analysis'),
]
