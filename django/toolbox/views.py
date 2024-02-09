import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes
import toolbox.climateFunctions as cf

from toolbox.serializers import ClimateFunctionSerializer, ClimateFunctionDetailSerializer, ClimateFunctionRequestSerializer, ExecuteResponseSerializer

INPUT_FOLDER_PATH = "data"
OUTPUT_FOLDER_PATH = "result_data"

def create_climate_function_list_4_api():
    """Creates a list of all functions available including id, name and function description

    Returns:
        list of dict: {id, name, description}
    """
    id = 0
    list = []
    for func in cf.ClimateFunctionList.list:
        list.append({"id": id, "name": func.name, "description": func.description})
        id += 1
    return list
        
def create_climate_function_details_4_api(id):
    """Creates a dictionary with detail information of function

    Args:
        id (int): id of function (number in list)

    Returns:
        dict: information for datasets and parameters of the function
    """
    func = cf.ClimateFunctionList.list[id]()
    return {'datasets':[vars(func.dataset_dict[key]) for key in func.dataset_dict], 'parameters':[vars(func.params_dict[key]) for key in func.params_dict]}
        
        
def create_dataset_path_list(dataset_name,input_folder):
    """
    Function needs to be replaced. Should return a string array with pathes of all datasets for a dataset name
    """
    
    
    return [os.path.join(input_folder, 'TIPPECC_CLMcom-KIT-CCLM5-0-15_v1_MPI-M-MPI-ESM-LR_tas_day_1950_2100.nc')]

class ClimateFunctionListAPIView(APIView):
    """Class for API View for climate function list

    Args:
        APIView: super class
    """
    @extend_schema(
        summary = 'Get all available climate functions',
        description = 'returns a list of all available climate functions',
        responses = ClimateFunctionSerializer(many=True))
    def get(self, request):
        """ returns data for the api if called

        Args:
            request (_type_): _description_

        Returns:
            json: list as json
        """
        queryset = cf.ClimateFunctionList.list
        serializer_class = ClimateFunctionSerializer
        serializer_data = serializer_class(queryset, many=True).data
        return JsonResponse(serializer_data, safe=False)
    
class ClimateFunctionDetailView(APIView):
    """Class for API View for climate function details

    Args:
        APIView: super class
    """
    @extend_schema(
        summary = 'Get details for climate function',
        description = 'Returns all information of a function by its id',
        parameters = [OpenApiParameter('id',OpenApiTypes.INT,OpenApiParameter.PATH,description='id of climate function')],
        responses = {
            200: OpenApiResponse(ClimateFunctionDetailSerializer(), description='success'),
            404: OpenApiResponse(description = 'id not found'),
            500: OpenApiResponse(description = 'internal server error')
        })
    def get(self, request, id):
        """ returns data for the api if called

        Args:
            request (_type_): _description_

        Returns:
            json: list as json
        """
        queryset = cf.ClimateFunctionList().get_func_by_id(id)
        
        if queryset == 0:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer_class = ClimateFunctionDetailSerializer
        if not serializer_class(queryset).is_valid:
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer_data = serializer_class(queryset).data
        return JsonResponse(serializer_data, safe=False)
    
    @extend_schema(summary = 'execute climate function',
        description = 'execute climate function by its id',
        parameters = [OpenApiParameter('id',OpenApiTypes.INT,OpenApiParameter.PATH,description='id of climate function')],
        request = ClimateFunctionRequestSerializer(),
        responses = {
            200: OpenApiResponse(ExecuteResponseSerializer, description='success'),
            500: OpenApiResponse(description = 'internal server error')
        })
    def post(self, request, id):
        """ returns data for the api if called

        Args:
            request (_type_): _description_

        Returns:
            json: list as json
        """
        
        serializer_data = ClimateFunctionRequestSerializer(data=request.data)
        print(serializer_data.initial_data)
        aoi = serializer_data.initial_data["aoi"]
        scene = cf.ClimateScene(aoi)
        selected_climate_func = cf.ClimateFunctionList().get_func_by_id(id)
        
        if selected_climate_func == 0: 
            print("Function not found")
        
        else:
            print("Function Selected")
            for dataset_name in serializer_data.initial_data["dataset_list"]:
                selected_climate_func.dataset_dict[dataset_name].set_path_list(create_dataset_path_list(dataset_name, INPUT_FOLDER_PATH))
            for key in serializer_data.initial_data["paramvalue_dict"]:
                selected_climate_func.params_dict[key].set_value(serializer_data.initial_data["paramvalue_dict"][key])

            selected_climate_func.set_climate_scene(scene)

        message, result_list = selected_climate_func.execute(OUTPUT_FOLDER_PATH)
        print(message)
        print(result_list)
        response_clas = cf.ExecuteResponse(id, message)
        print(ExecuteResponseSerializer(response_clas).data)
        return JsonResponse(ExecuteResponseSerializer(response_clas).data, safe=False)


