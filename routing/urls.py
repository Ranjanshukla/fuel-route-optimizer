from django.urls import path
from routing.views import OptimizeRouteAPIView

urlpatterns = [
    path(
        "optimize/",OptimizeRouteAPIView.as_view(),name="optimize-route")
]