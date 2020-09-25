from rest_framework import serializers

from .models import Videos #, Keys

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
        # fields = ('title','description')

# class KeysSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Keys
#         fields = '__all__'