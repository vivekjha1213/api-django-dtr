from datetime import datetime

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = datetime.now()
        response = self.get_response(request)
        end_time = datetime.now()
        processing_time = end_time - request.start_time
        print(f"Time taken for request: {processing_time}")
        return response
