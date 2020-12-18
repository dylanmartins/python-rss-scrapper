from django.urls import path
from feeds.views import HelloView

urlpatterns = [
    path('', HelloView.as_view(), name='hello'),
]
