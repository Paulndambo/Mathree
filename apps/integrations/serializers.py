from rest_framework import serializers


class SasaPayCallbackSerializer(serializers.Serializer):
    body = serializers.JSONField(default=dict)