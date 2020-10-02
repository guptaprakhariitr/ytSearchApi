from rest_framework import serializers
from .models import ytVideo

class VidSerializer(serializers.ModelSerializer):
    class Meta:
        model = ytVideo
        fields = '__all__'