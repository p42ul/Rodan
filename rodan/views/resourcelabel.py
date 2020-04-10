from rest_framework import generics

from rodan.models import ResourceLabel
from rodan.permissions import CustomObjectPermissions


class ResourceLabelDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  """
  permission_classes = (permissions.IsAuthenticated, CustomObjectPermissions)
  queryset = ResourceLabel.objects.all()