from rest_framework import serializers

from .models import KBEntry


class KBQuerySerializer(serializers.Serializer):
    """Validates the incoming search request body."""
    search = serializers.CharField()


class KBEntrySerializer(serializers.ModelSerializer):
    """Shapes a single KB entry for the response (no created_at)."""
    class Meta:
        model = KBEntry
        fields = ["id", "question", "answer", "category"]
