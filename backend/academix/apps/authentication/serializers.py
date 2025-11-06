# third-party imports
from rest_framework import serializers;

# local imports
from .models import User;
from apps.administration.models import College;

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User;
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'college', 'is_active', 'date_joined'];
        read_only_fields = ['id', 'date_joined', 'is_active'];
        
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8);
    
    class Meta:
        model = User;
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'college'];
        read_only_fields = ['id'];
        
    def validate_college(self, value):
        # ensure college exists if provided
        if value is None:
            return value;
        if not College.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("College Not Found");
        
        return value;
    
    def create(self, validate_data):
        password = validate_data.pop('password');
        
        user = User.objects.create_user(password=password, **validate_data);
        return user;
    
class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User;
        fields = ['first_name', 'last_name', 'role', 'college', 'is_active'];
        read_only_fields = [];