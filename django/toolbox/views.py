from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
import toolbox.climateFunctions as cf




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
        
class ClimateFunctionListAPIView(APIView):
    """Class for API View for climate function list

    Args:
        APIView: super class
    """
    def get(self, request):
        """ returns data for the api if called

        Args:
            request (_type_): _description_

        Returns:
            json: list as json
        """
        data = create_climate_function_list_4_api()
        return JsonResponse(data, safe=False)

class ClimateFunctionDetailView(APIView):
    """Class for API View for climate function details

    Args:
        APIView: super class
    """
    def get(self, request, id):
        """ returns data for the api if called

        Args:
            request (_type_): _description_

        Returns:
            json: list as json
        """
        data = create_climate_function_details_4_api(id)
        return JsonResponse(data, safe=False)


