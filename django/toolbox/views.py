from django.shortcuts import render
from rest_framework import generics
from toolbox.models import ClimateIndicesFunction
from toolbox.serializers import ClimateIndicesFunctionSerializer


class ClimateIndicesFunctionListAPIView(generics.ListAPIView):
    queryset = ClimateIndicesFunction.objects.all()
    serializer_class = ClimateIndicesFunctionSerializer

# Create your views here.
from toolbox.models import ClimateIndicesFunction

# # Create an instance of the model
# new_instance = ClimateIndicesFunction

# # Set values for the fields
# new_instance.name = "heat days"

# # Save the instance to the database
# new_instance.save()

# # Create an instance of the model
# new_instance = ClimateIndicesFunction

# # Set values for the fields
# new_instance.name = "dry days"

# # Save the instance to the database
# new_instance.save()