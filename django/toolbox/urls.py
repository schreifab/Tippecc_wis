from django.urls import path
from toolbox.views import ClimateFunctionListAPIView, ClimateFunctionDetailView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('climate-indices/', ClimateFunctionListAPIView.as_view(), name='climate_indices_list'),
    path('climate-indices/<int:id>', ClimateFunctionDetailView.as_view(), name='climate_indices_details'),
    # Add other URL patterns as needed
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]