from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from items.services import ItemsManagerService


class ItemsFeedView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        self.manager = ItemsManagerService()

    def get(self, request, uuid_feed):
        show_all_read = request.GET.get('show_all_read')
        show_all_unread = request.GET.get('show_all_unread')
        content = {
            'data': self.manager.get_all_items_by_feed(
                uuid_feed,
                request.user,
                show_all_read,
                show_all_unread
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
