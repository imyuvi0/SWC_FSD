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
    import os, traceback
    from django.conf import settings
    db_status = "Unknown"
    static_status = "Unknown"

    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = "Connected successfully!"
    except Exception as e:
        db_status = f"Failed: {str(e)}"

    try:
        from django.contrib.staticfiles.storage import staticfiles_storage
        static_status = f"Storage: {staticfiles_storage.__class__.__name__}"
        manifest_path = os.path.join(settings.STATIC_ROOT, 'staticfiles.json')
        static_status += f" | Static Root: {settings.STATIC_ROOT} | Manifest Exists: {os.path.exists(manifest_path)}"
        if os.path.exists(settings.STATIC_ROOT):
            static_status += f" | Files: {os.listdir(settings.STATIC_ROOT)}"
    except Exception as e:
        static_status = f"Static check failed: {str(e)}"

    return JsonResponse({
        "message": "Welcome to the Game Key Platform API backend!",
        "version": "1.0",
        "db_status": db_status,
        "static_status": static_status,
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
