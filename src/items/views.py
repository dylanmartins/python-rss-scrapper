from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from items.services import ItemsManagerService


class ItemsFeedView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = ItemsManagerService()

    def get(self, request, uuid_feed):
        content = {
            'data': self.manager.get_all_items_by_feed(
                uuid_feed,
                request.user
            )
        }
        return JsonResponse(content, status=200)


class ReadItemView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = ItemsManagerService()

    def get(self, request, uuid_item):
        content = {
            'data': self.manager.get_item_and_set_is_read(
                uuid_item,
                request.user
            )
        }
        return JsonResponse(content, status=200)
