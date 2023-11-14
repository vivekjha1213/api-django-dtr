from django.core.mail import send_mail


class AdminNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the path of the endpoint that was requested
        endpoint_path = request.path

     
        print(f"Endpoint Path: {endpoint_path}")

        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            subject = 'Admin Notification'
            message = 'A notification from your Django app.'
            from_email = 'vivek.jha@dtroffle.com'

            recipient_list = ['admin@example.com', 'vivekjha1213@gmail.com']

            send_mail(subject, message, from_email, recipient_list)

        response = self.get_response(request)
        return response
