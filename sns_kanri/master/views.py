from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from sns_kanri.master.models import User
from sns_kanri.master.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """カテゴリーのview_set"""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.request.user.id)
        return queryset
