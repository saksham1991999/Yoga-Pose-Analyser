from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from pose_analyser.views import PoseViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="Yoga Pose Analyser",
      default_version='v1',
      description="Find your Fitness Buddy.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@gymbuddyindia.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
# router.register('users', UserAPIView, basename='user')
router.register(r'poses', PoseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('core/', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('social/', include('social.urls')),

    path('api/', include(router.urls)),
    path('', include('pose_analyser.urls')),
    # path('users/', UserAPIView.as_view())
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
