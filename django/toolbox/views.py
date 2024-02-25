import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers
import requests

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes
import toolbox.models as cf
from toolbox.climateFunctions import ClimateFunctionList

from toolbox.serializers import ClimateFunctionSerializer, ClimateFunctionDetailSerializer, ClimateFunctionRequestSerializer, ExecuteResponseSerializer

#INPUT_FOLDER_PATH = "data"
OUTPUT_FOLDER_PATH = "result_data"
PATH_API_URL = "https://leutra.geogr.uni-jena.de/backend_geoportal/climate/download?"

# ad ds if xclim name and datafile name are not the same
# left: xclim name/ key in ClimateDataset right: filename
dataset_name_correction_list = {
    'sfcWind': 'sfcwind'
}

        
def create_dataset_path_dict(dataset_name,file_id_list):
    """
    Function needs to be replaced. Should return a string array with pathes of all datasets for a dataset name
    """
    # changes the name of the dataset if theyre not compatible with the xclim names here
    path_dict = {}
    
    if dataset_name in dataset_name_correction_list:
        dataset_name = dataset_name_correction_list[dataset_name]
    for file in file_id_list:
        file_split = file.split("_")
        if dataset_name == file_split[0]:
            path_dict[file_split[1]] = requests.get(PATH_API_URL +  "id=" + file_split[2] + "&path=true").text
    print(path_dict)
    return path_dict

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
        queryset = ClimateFunctionList.list
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
        queryset = ClimateFunctionList().get_func_by_id(id)
        
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
        """ 
        The Main method for the workflow. 
        Is triggered by Submit of the user. 
        Get the data from the ui as ClimateFunctionRequest
        

        Args:
            id: int
                func id

        Returns:
            json:
                Serialized data of Execute Respsonse
        """
        
        serializer_data = ClimateFunctionRequestSerializer(data=request.data)
        print(serializer_data.initial_data)
        #climate Scene
        aoi = serializer_data.initial_data["aoi"]
        scene = cf.ClimateScene(aoi)
        file_id_list = serializer_data.initial_data["file_id_list"]
        #get function
        selected_climate_func = ClimateFunctionList().get_func_by_id(id)
        
        #create return objects
        message = ""
        result_list = []
        
        if selected_climate_func == 0: 
            message = "404 function not found"
        
        #set paths values and scene
        else:
            try:
                print("Function Selected")
                for dataset_name in serializer_data.initial_data["dataset_list"]:
                    selected_climate_func.dataset_dict[dataset_name].set_path_dict(create_dataset_path_dict(dataset_name, file_id_list))
                for key in serializer_data.initial_data["paramvalue_dict"]:
                    selected_climate_func.params_dict[key].set_value(serializer_data.initial_data["paramvalue_dict"][key])
                selected_climate_func.set_climate_scene(scene)
            except Exception as e:
                message = str(e)

        print(message)            

        #execute the function 
        if(message == ""):
            message, result_list = selected_climate_func.execute(OUTPUT_FOLDER_PATH)
        print(message)
        print(result_list)
        response_clas = cf.ExecuteResponse(id, message)
        return JsonResponse(ExecuteResponseSerializer(response_clas).data, safe=False)


