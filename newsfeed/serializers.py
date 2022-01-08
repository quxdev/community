from .models import Newsitem, Vote, Comment
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class NewsitemSerializer(ModelSerializer):
    class Meta:
        model = Newsitem
        fields = '__all__'

        