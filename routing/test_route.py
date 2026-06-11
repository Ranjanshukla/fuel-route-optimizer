from routing.services.openroute_service import OpenRouteService


service = OpenRouteService()

route = service.get_route(
    [-96.7970, 32.7767],   # Dallas
    [-87.6298, 41.8781]    # Chicago
)

print(route)