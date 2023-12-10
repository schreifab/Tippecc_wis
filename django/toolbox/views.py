from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from toolbox.models import ClimateIndicesFunction
from toolbox.serializers import ClimateIndicesFunctionSerializer
import toolbox.climateFunctions as cf
import json



def create_climate_function_list_4_api():
    id = 0
    list = []
    for func in cf.ClimateFunctionList.list:
        list.append({"id": id, "name": func.name, "description": func.description})
        id += 1
    return list
        
def create_climate_function_details_4_api(id):
    func = cf.ClimateFunctionList.list[id]()
    return {'datasets':[vars(func.dataset_dict[key]) for key in func.dataset_dict], 'parameters':[vars(func.params_dict[key]) for key in func.params_dict]}
        


class ClimateIndicesFunctionListAPIView(generics.ListAPIView):
    queryset = ClimateIndicesFunction.objects.all()
    serializer_class = ClimateIndicesFunctionSerializer

class ClimateFunctionListAPIView(APIView):
    def get(self, request):
        data = create_climate_function_list_4_api()
        return JsonResponse(data, safe=False)

class ClimateFunctionDetailView(APIView):
    def get(self, request, id):
        data = create_climate_function_details_4_api(id)
        return JsonResponse(data, safe=False)

# Create your views here.
from toolbox.models import ClimateIndicesFunction

