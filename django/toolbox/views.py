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
        


class ClimateIndicesFunctionListAPIView(generics.ListAPIView):
    queryset = ClimateIndicesFunction.objects.all()
    serializer_class = ClimateIndicesFunctionSerializer

class ClimateFunctionListAPIView(APIView):
    def get(self, request):
        # Perform necessary operations
        data = create_climate_function_list_4_api()
        return JsonResponse(data, safe=False)

# Create your views here.
from toolbox.models import ClimateIndicesFunction

