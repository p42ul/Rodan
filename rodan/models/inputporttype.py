from django.db import models
from uuidfield import UUIDField


class InputPortType(models.Model):
    class Meta:
        app_label = 'rodan'

    uuid = UUIDField(primary_key=True, auto=True)
    job = models.ForeignKey('rodan.Job', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    resource_type = models.CharField(max_length=20)
    minimum = models.IntegerField()
    maximum = models.IntegerField()

    def __unicode__(self):
        return u"<InputPortType {0}>".format(str(self.uuid))
