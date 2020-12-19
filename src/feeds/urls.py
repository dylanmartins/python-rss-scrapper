from django.urls import path
from feeds.views import FeedsView

urlpatterns = [
    path('', FeedsView.as_view(), name='index'),
]
