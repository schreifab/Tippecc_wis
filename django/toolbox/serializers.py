
from rest_framework import serializers
from toolbox.models import ClimateFunction, ClimateDataset, ClimateParameter, ClimateFunctionRequest, ClimateScene, ExecuteResponse

#All Serilizer classes here

class StringListField(serializers.ListField):
    child = serializers.CharField()

class FloatListField(serializers.ListField):
    child = serializers.FloatField()

class ClimateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateDataset
        fields = ("name", "desc", "filter_word", "optional")

class ClimateParameterSerializer(serializers.ModelSerializer):
    input_list = StringListField()
    unit_list = StringListField()

    class Meta:
        model = ClimateParameter
        fields = ("name", "desc", "datatype", "input_list", "unit_list", "optional")

class ClimateFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateFunction
        fields = ("id", "name", "description")

class ClimateFunctionDetailSerializer(serializers.ModelSerializer):

    dataset_dict = serializers.DictField(child = ClimateDatasetSerializer())
    params_dict = serializers.DictField(child = ClimateParameterSerializer())

    class Meta:
        model = ClimateFunction
        fields = ("id", "dataset_dict", "params_dict")

class ClimateFunctionRequestSerializer(serializers.ModelSerializer):
    dataset_list = StringListField()
    paramvalue_dict =  serializers.DictField()
    aoi = FloatListField()
    file_id_list = StringListField()
    class Meta:
        model = ClimateFunctionRequest
        fields = ("dataset_list","paramvalue_dict","aoi","file_id_list")

class ExecuteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecuteResponse
        fields = '__all__'