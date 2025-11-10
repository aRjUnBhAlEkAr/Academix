# third-party imports
from rest_framework import serializers;

# local imports
from .models import Teacher;
from apps.authentication.models import User;

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User;
        fields = ['email', 'first_name', 'last_name'];

class TeacherReadSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True);
    
    class Meta:
        model = Teacher;
        fields = ['id', 'user', 'employee_id', 'department', 'hired_date', 'is_active'];
        
class TeacherCreateSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer();
    password = serializers.CharField(write_only=True, min_length=6);
    
    class Meta:
        model = Teacher;
        fields = ['id', 'user', 'password', 'employee_id', 'department', 'hired_at', 'is_active'];
        
    def validate_user(self, user):
        if User.objects.filter(email=value.get('email')).exists():
            raise serializers.ValidationError("User with this email already exists.");
        return value;
    
    def create(self, validated_data):
        user_data = validate_data.pop('user');
        password = validate_date.pop('password');
        
        request_user = self.context['request'].user;
        college = getattr(request_user, 'college', None);
        
        user = User.objects.create(
            email = user_data['email'],
            first_name = user_data.get('first_name', ''),
            last_name = user_data.get('last_name', ''),
            role='teacher',
            college = college
        )
        user.set_password(password);
        user.save();
        
        teacher = Teacher.objects.create(user=user, **validate_data);
        return teacher;
    
class TeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher;
        fields = ['employee_id', 'department', 'hired_date', 'is_active'];