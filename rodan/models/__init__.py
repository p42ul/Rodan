from rodan.models.inputporttype import InputPortType
from rodan.models.outputporttype import OutputPortType
from rodan.models.inputport import InputPort
from rodan.models.outputport import OutputPort
from rodan.models.input import Input
from rodan.models.output import Output
from rodan.models.project import Project
from rodan.models.job import Job
from rodan.models.workflowjob import WorkflowJob
from rodan.models.workflow import Workflow
from rodan.models.workflowrun import WorkflowRun
from rodan.models.runjob import RunJob
from rodan.models.resultspackage import ResultsPackage
from rodan.models.resource import Resource
from rodan.models.resourcetype import ResourceType
from rodan.models.connection import Connection

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json
import psycopg2
import psycopg2.extensions

@receiver(post_save)
def notify_socket_subscribers(sender, instance, created, **kwargs):
    publisher = RedisPublisher(facility='rodan', broadcast=True)
    status = "created" if created else "updated"
    uuid = "{0}".format(instance.uuid) if hasattr(instance, "uuid") else ""
    data = {
        'status': status,
        'model': instance.__class__.__name__,
        'uuid': uuid
    }
    message = RedisMessage(json.dumps(data))
    publisher.publish_message(message)

