from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ShareViewSet, ShareQueriedViewSet

app_name = 'share'
router = DefaultRouter()
router.register(r'', ShareViewSet, basename='share')
# names: http://www.tomchristie.com/rest-framework-2-docs/api-guide/routers

urlpatterns = [
    path('q/', ShareQueriedViewSet.as_view({'get': 'list'}), name='share_query'),
] + router.urls
