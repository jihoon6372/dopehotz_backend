from rest_framework import serializers
from .models import *

class DiscordLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DiscordLog
        fields = (
            'log_message',
            'created_at'
		)

        read_only_fields = (
            'created_at',
        )