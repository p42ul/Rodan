# from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rodan.serializers.project import ProjectSerializer
from rodan.serializers.user import UserSerializer
from rodan.serializers.page import PageSerializer

from rodan.models.project import Project
from rodan.models.workflow import Workflow
from rodan.models.workflowjob import WorkflowJob
from rodan.models.page import Page
from rodan.models.job import Job
from rodan.models.result import Result


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
            'projects': reverse('project-list', request=request, format=format),
            'workflows': reverse('workflow-list', request=request, format=format),
            'workflowjobs': reverse('workflowjob-list', request=request, format=format),
            'pages': reverse('page-list', request=request, format=format),
            'jobs': reverse('job-list', request=request, format=format),
            'results': reverse('result-list', request=request, format=format),
            'users': reverse('user-list', request=request, format=format)
        })


@ensure_csrf_cookie
def home(request):
    data = {}
    return render(request, 'base.html', data)


class ProjectList(generics.ListCreateAPIView):
    model = Project
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ProjectSerializer

    def pre_save(self, obj):
        obj.creator = self.request.user


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Project
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ProjectSerializer

    def pre_save(self, obj):
        obj.creator = self.request.user


class WorkflowList(generics.ListCreateAPIView):
    model = Workflow
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # serializer_class = UserSerializer

    def pre_save(self, obj):
        pass


class WorkflowDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Workflow
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # serializer_class = UserSerializer

    def pre_save(self, obj):
        pass


class WorkflowJobList(generics.ListCreateAPIView):
    model = WorkflowJob


class WorkflowJobDetail(generics.RetrieveUpdateDestroyAPIView):
    model = WorkflowJob


class PageList(generics.ListCreateAPIView):
    model = Page
    permission_classes = (permissions.AllowAny, )
    serializer_class = PageSerializer

    # override the POST method to deal with multiple files in a single request
    def post(self, request, *args, **kwargs):
        if not request.FILES:
            return Response({'error': "You must supply at least one file to upload"}, status=status.HTTP_400_BAD_REQUEST)
        response = []
        for seq, fileobj in enumerate(request.FILES.getlist('files')):
            data = {
                'project': request.POST['project'],
                'page_order': seq,
            }

            files = {
                'page_image': fileobj
            }
            serializer = PageSerializer(data=data, files=files)

            if serializer.is_valid():
                self.object = serializer.save()
                response.append(serializer.data)
            else:
                # if there's an error, bail early and send the error back to the client
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'pages': response}, status=status.HTTP_201_CREATED)


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Page
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = PageSerializer


class JobList(generics.ListCreateAPIView):
    model = Job


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Job


class ResultList(generics.ListCreateAPIView):
    model = Result


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Result


class UserList(generics.ListCreateAPIView):
    model = User
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = UserSerializer
