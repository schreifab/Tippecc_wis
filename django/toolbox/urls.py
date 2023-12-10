from django.urls import path
from toolbox.views import ClimateFunctionListAPIView, ClimateFunctionDetailView

urlpatterns = [
    path('climate-indices/', ClimateFunctionListAPIView.as_view(), name='climate_indices_list'),
    path('climate-indices/<int:id>', ClimateFunctionDetailView.as_view(), name='climate_indices_details')
    # Add other URL patterns as needed
]