from rodan.models.project import Project
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name="user-detail")
    # pages = serializers.HyperlinkedRelatedField(view_name="page-detail")

    class Meta:
        model = Project
        fields = ("url", "name", "description", "creator")
