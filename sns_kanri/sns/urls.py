from rest_framework.routers import DefaultRouter

from sns_kanri.sns.views import RecordViewSet, SNSViewSet

router = DefaultRouter()
router.register('sns', SNSViewSet)
router.register('record', RecordViewSet)
