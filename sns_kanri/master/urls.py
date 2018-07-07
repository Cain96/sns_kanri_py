from rest_framework.routers import DefaultRouter

from sns_kanri.master.views import UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
