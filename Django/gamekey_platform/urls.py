from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from games.viewsets import GameViewSet, PublisherViewSet
from games.views import register, purchase_key

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'publishers', PublisherViewSet)

def api_root(request):
    import traceback
    db_status = "Unknown"
    error_trace = ""
    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = "Connected successfully!"
        
        from games.models import Game
        list(Game.objects.all())
        db_status += " (Query succeeded!)"
    except Exception as e:
        db_status = f"Connection/Query failed: {str(e)}"
        error_trace = traceback.format_exc()

    return JsonResponse({
        "message": "Welcome to the Game Key Platform API backend!",
        "version": "1.0",
        "db_status": db_status,
        "error_trace": error_trace,
        "endpoints": {
            "games": "/api/games/",
            "publishers": "/api/publishers/",
            "register": "/api/register/",
            "orders": "/api/orders/",
            "admin": "/admin/"
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register, name='register'),
    path('api/orders/', purchase_key, name='purchase_key'),
]
