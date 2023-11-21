from django.urls import path
from toolbox.views import ClimateIndicesFunctionListAPIView

urlpatterns = [
    path('climate-indices/', ClimateIndicesFunctionListAPIView.as_view(), name='climate_indices_list'),
    # Add other URL patterns as needed
]