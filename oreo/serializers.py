from rest_framework import serializers
from abc import ABC

from .models import Message


class DateField(serializers.Field, ABC):
    """
    serializer to serialize models.DateField value to more friendly format
    """

    def to_representation(self, value):
        return value.strftime("%d %b, %Y - %Hh%Mm")


class MessageSerializer(serializers.ModelSerializer):
    """
    serializer to serialize Message model instance from queryset to
    OrderedDict
    """

    created = DateField(read_only=True)
    updated = DateField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
