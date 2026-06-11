
from rest_framework import serializers

class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)