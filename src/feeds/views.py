import json

from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feeds.models import Feed
from feeds.serializers import CreateFeedSerializer
from feeds.services import FeedsManagerService


class FeedsView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def get(self, request):
        content = {
            'data': self.manager.get_all_feeds_by_user(request.user)
        }
        return JsonResponse(content, status=200)


class ManageFeedsView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = CreateFeedSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data['follower'] = request.user

        created = self.manager.get_or_create_feed(validated_data)

        status = 201 if created else 409
        return HttpResponse(status=status)

    def delete(self, request, uuid):
        deleted = self.manager.delete_feed(uuid)
        status = 200 if deleted else 400
        return HttpResponse(status=status)
