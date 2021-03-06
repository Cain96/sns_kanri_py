"""sns_kanri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from sns_kanri import settings
from sns_kanri.master.urls import router as master_router
from sns_kanri.sns.urls import (
    router as sns_router, statistic_urlpatterns, time_urlpatterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_jwt_token),
    path('api/', include(sns_router.urls)),
    path('api/', include(master_router.urls)),
    path('api/statistic/', include(statistic_urlpatterns)),
    path('api/time/', include(time_urlpatterns))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
