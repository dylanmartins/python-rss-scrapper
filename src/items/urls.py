from django.urls import path
from items import views

urlpatterns = [
    path('feed/<uuid:uuid_feed>/', views.ItemsFeedView.as_view(), name='index'),
]
