class AutoMigrateMiddleware:
    _migrated = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not AutoMigrateMiddleware._migrated:
            from django.core.management import call_command
            try:
                # Run database migrations on the first request to this container
                call_command('migrate', interactive=False)
                AutoMigrateMiddleware._migrated = True

                # Pre-configure admin user and default frontend testing token
                from django.contrib.auth.models import User
                from rest_framework.authtoken.models import Token
                
                if not User.objects.filter(username='admin').exists():
                    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                    Token.objects.get_or_create(user=admin_user, key='8bdecdaffb820e0d53abbbc8c8fe0ca69b3e8e88')
            except Exception as e:
                # Log any failure to console
                print("Auto-migration or user setup failed in middleware:", e)
        return self.get_response(request)
