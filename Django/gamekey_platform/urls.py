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
    from io import StringIO
    from django.core.management import call_command
    
    migrate_out = StringIO()
    migrate_err = StringIO()
    db_status = "Unknown"
    
    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = "Connected."
        
        # Trigger migrations on-demand and capture stdout/stderr
        call_command('migrate', interactive=False, stdout=migrate_out, stderr=migrate_err)
        db_status += " Migration run complete!"
    except Exception as e:
        db_status += f" Migration failed: {str(e)}"

    return JsonResponse({
        "message": "Welcome to the Game Key Platform API backend!",
        "version": "1.0",
        "db_status": db_status,
        "migrate_stdout": migrate_out.getvalue(),
        "migrate_stderr": migrate_err.getvalue(),

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
