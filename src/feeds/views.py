
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from feeds.serializers import CreateFeedSerializer
from feeds.services import FeedsManagerService


class FeedsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def get(self, request):
        content = {
            'data': self.manager.get_all_feeds_by_user(request.user)
        }
        return JsonResponse(content, status=200)


class CreateFeedsView(GenericAPIView):
    serializer_class = CreateFeedSerializer
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data['follower'] = request.user

        created = self.manager.get_or_create_feed(validated_data)

        status = 201 if created else 409
        return HttpResponse(status=status)


class DeleteFeedsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def delete(self, request, uuid):
        deleted = self.manager.delete_feed(uuid, request.user)
        status = 204 if deleted else 400
        return HttpResponse(status=status)


class UpdateFeedsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = FeedsManagerService()

    def get(self, request, uuid):
        self.manager.update_feed(uuid, request.user)
        return HttpResponse(status=204)
