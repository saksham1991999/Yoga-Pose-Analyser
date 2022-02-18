from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'core'

router = DefaultRouter()
# router.register('posts', views.PostViewSet, basename='posts')
urlpatterns = router.urls
