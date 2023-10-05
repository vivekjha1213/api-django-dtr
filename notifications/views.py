from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import status
from rest_framework.response import Response

class CustomNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.all()
        return queryset


class ClientNotificationListView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        recipient_id = self.kwargs.get('recipient_id')
        queryset = Notification.objects.filter(recipient_id=recipient_id)
        return queryset

    def create(self, request, *args, **kwargs):
        recipient_id = request.data.get('recipient_id')

        if recipient_id is None:
            return Response(
                {"error": "recipient_id is required in the request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipient = Notification.objects.filter(recipient_id=recipient_id).first()

        if not recipient:
            return Response(
                {"error": "Recipient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        queryset = Notification.objects.filter(recipient_id=recipient_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)