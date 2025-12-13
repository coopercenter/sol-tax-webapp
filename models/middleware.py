from django.conf import settings
from django.shortcuts import render

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow admin access
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Allow static files
        if request.path.startswith("/static/"):
            return self.get_response(request)

        if getattr(settings, "MAINTENANCE_MODE", False):
            return render(request, "maintenance.html", status=503)

        return self.get_response(request)
