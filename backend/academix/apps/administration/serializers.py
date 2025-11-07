from rest_framework import serializers
from .models import College
from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name', 'code', 'address', 'active', 'created_at']
        read_only_fields = ['id', 'created_at']

class AssignCollegeAdminSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        if user.role != 'college_admin':
            raise serializers.ValidationError("User must have role 'college_admin' to be assigned as a college admin")
        return value
