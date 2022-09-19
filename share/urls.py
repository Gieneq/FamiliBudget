from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ShareViewSet, ShareQueriedViewSet

app_name = 'share'
router = DefaultRouter()
router.register(r'', ShareViewSet, basename='share')
# names: http://www.tomchristie.com/rest-framework-2-docs/api-guide/routers
# (r'^user/(?P<username>\w{0,50})/$', views.profile_page,),
urlpatterns = [
    path('', ShareQueriedViewSet.as_view({'get': 'list'}), name='share_query'),
    # path('profile/<slug:slug>/contributing/', ShareByProfileViewSet.as_view({'get': 'list'}), name='share_byprofile')
] + router.urls

# path('profile/<slug:slug>/share/', include('share.urls', namespace='shared_to')),