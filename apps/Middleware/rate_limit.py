import time
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def rate_limit(self, request, rate_limit, per_minute):
        ip = request.META.get("REMOTE_ADDR")

        current_time = int(time.time())

        if ip not in self.requests:
            self.requests[ip] = []

        self.requests[ip] = [
            r for r in self.requests[ip] if r > current_time - per_minute
        ]

        if len(self.requests[ip]) >= rate_limit:
            return HttpResponseForbidden("Rate limit exceeded")

        self.requests[ip].append(current_time)

    def __call__(self, request):
        # Check if the view has a custom rate limit attribute
        rate_limit = getattr(request, 'rate_limit', None)
        per_minute = 60  # Default per-minute rate limit

        if rate_limit is not None:
            self.rate_limit(request, rate_limit=rate_limit, per_minute=per_minute)

        response = self.get_response(request)
        return response
