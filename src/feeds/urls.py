from django.urls import path

from feeds import views

urlpatterns = [
    path('', views.FeedsView.as_view(), name='index'),
    path('create/', views.CreateFeedsView.as_view(), name='create'),
    path(
        '<uuid:uuid>/delete/',
        views.DeleteFeedsView.as_view(),
        name='delete'
    ),
]
