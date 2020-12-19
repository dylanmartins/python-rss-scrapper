import json

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class FeedsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': f'Welcome {request.user}'}
        return JsonResponse(content, status=200)
