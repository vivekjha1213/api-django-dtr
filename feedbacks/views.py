from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feedback
from .serializers import FeedbackSerializerCreate, FeedbackSerializerList, FeedbackSerializerUpdate

class CreateFeedbackView(APIView):
    def post(self, request, format=None):
        serializer = FeedbackSerializerCreate(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ListFeedbackView(APIView):
    def get(self, request, id=None, format=None):
        if id is None:
            # List all feedback instances
            feedback = Feedback.objects.all()
            serializer = FeedbackSerializerList(feedback, many=True)
            return Response(serializer.data)
        

    
class RetrieveFeedbackView(APIView):
    def get(self, request, format=None):
        pk = request.query_params.get('id')

        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            feedback = Feedback.objects.get(pk=pk)
            serializer = FeedbackSerializerList(feedback)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    

class TotalFeedbackView(APIView):
    def get(self, request, format=None):
        total_feedback_count = Feedback.objects.count()
        return Response({"total_count": total_feedback_count})    
        
        
        
class UpdateFeedbackView(APIView):
    def put(self, request, pk, format=None):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializerUpdate(feedback, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializerUpdate(feedback, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class DeleteFeedbackView(APIView):
    def delete(self, request, pk, format=None):
        try:
            feedback = Feedback.objects.get(pk=pk)
            deleted_feedback = feedback.delete()
            if deleted_feedback:
                return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Feedback could not be deleted"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Feedback.DoesNotExist:
            return Response({"error": "Feedback with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
