# third-party import
from rest_framework import serializers

# local imports
from .models import Student
from apps.authentication.models import User


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class StudentCreateSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer();
    password = serializers.CharField(write_only=True, min_length=6);

    class Meta:
        model = Student;
        fields = ['id', 'user', 'password', 'roll_number', 'department', 'year', 'is_active'];

    def create(self, validated_data):
        user_data = validated_data.pop('user');
        password = validated_data.pop('password');

        request_user = self.context['request'].user;
        college = getattr(request_user, 'college', None);

        user = User.objects.create(
            email=user_data['email'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            role='student',
            college=college
        )
        user.set_password(password);
        user.save();

        student = Student.objects.create(user=user, **validated_data);
        return student;


class StudentReadSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True);

    class Meta:
        model = Student
        fields = ['id', 'user', 'roll_number', 'department', 'year', 'is_active']