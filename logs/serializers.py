from rest_framework import serializers

class SetFolderSerializer(serializers.Serializer):
    folder = serializers.CharField(max_length=255)