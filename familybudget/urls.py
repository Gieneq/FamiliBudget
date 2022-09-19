"""familybudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(('GET',))
def api_info_view(request):
    content = {
        # 'help': reverse('apihelp', request=request),
        'user': str(reverse('userprofile:user_list', request=request)),
        'profile': str(reverse('userprofile:userprofile_list', request=request)),
        'share': str(reverse('share:share-list', request=request)),
        #todo budgets
    }
    return Response(content)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', api_info_view, name='apihelp'),
    path('api/v1/user/', include('userprofile.urls', namespace='userprofile')),
    path('api/v1/share/', include('share.urls', namespace='share')),
    # path('api/v1/shared_to/', include('share.urls', namespace='share')),
]
