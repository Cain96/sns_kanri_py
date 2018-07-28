from django.urls import path
from rest_framework.routers import DefaultRouter

from sns_kanri.sns import views
from sns_kanri.sns.views import RecordViewSet, SNSViewSet

router = DefaultRouter()
router.register('sns', SNSViewSet)
router.register('record', RecordViewSet)

statistic_urlpatterns = [
    path('', views.StatisticView.as_view(), name='list')
]

time_urlpatterns = [
    path('', views.TimeView.as_view(), name='list')
]
