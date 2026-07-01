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
            except Exception as e:
                # Log any failure to console
                print("Auto-migration failed in middleware:", e)
        return self.get_response(request)
