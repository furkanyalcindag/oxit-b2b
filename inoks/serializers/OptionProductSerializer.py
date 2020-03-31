from rest_framework import serializers

from inoks.models import OptionProduct


class OptionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionProduct
        fields = '__all__'
        depth = 3
