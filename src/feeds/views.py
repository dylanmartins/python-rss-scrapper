import json

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
