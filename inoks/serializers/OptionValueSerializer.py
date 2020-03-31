from rest_framework import serializers

from inoks.models import OptionProduct, OptionValue


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'
        depth = 3
