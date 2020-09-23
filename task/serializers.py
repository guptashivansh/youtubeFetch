from rest_framework import serializers

from .models import Videos

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
        # fields = ('title','description')