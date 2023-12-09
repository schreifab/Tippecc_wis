from django.urls import path
from toolbox.views import ClimateFunctionListAPIView

urlpatterns = [
    path('climate-indices/', ClimateFunctionListAPIView.as_view(), name='climate_indices_list'),
    # Add other URL patterns as needed
]