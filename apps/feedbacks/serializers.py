from rest_framework import serializers
from .models import Feedback



class FeedbackSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['email', 'notes','client']

    def validate_email(self, value):
        # Check if an existing feedback with the same email already exists
        if Feedback.objects.filter(email=value).exists():
            raise serializers.ValidationError("A feedback with this email already exists.")
        return value




class FeedbackSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'



class FeedbackSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['email', 'notes','client']