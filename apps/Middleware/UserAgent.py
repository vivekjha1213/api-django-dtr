class CustomUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        request.META['HTTP_USER_AGENT']

        response = self.get_response(request)

        print("User-Agent:", request.META.get('HTTP_USER_AGENT'))

        return response
