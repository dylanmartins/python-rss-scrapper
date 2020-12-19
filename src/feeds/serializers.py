from rest_framework import serializers


class CreateFeedSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    url = serializers.URLField()
