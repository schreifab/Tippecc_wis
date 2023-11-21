
from rest_framework import serializers
from toolbox.models import ClimateIndicesFunction

class ClimateIndicesFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateIndicesFunction
        fields = ['id', 'name']
