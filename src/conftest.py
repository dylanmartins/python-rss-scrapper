import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def normal_user_a():
    return User.objects.create_user(
        username='userA',
        email='userA@foo.com',
        password='pass'
    )


@pytest.fixture
def normal_user_b():
    return User.objects.create_user(
        username='userB',
        email='userB@foo.com',
        password='pass'
    )


@pytest.fixture
def api_client(normal_user_a):
    client = APIClient()
    refresh = RefreshToken.for_user(normal_user_a)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
