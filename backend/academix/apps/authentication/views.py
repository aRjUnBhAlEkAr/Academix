# third-party packge import
from rest_framework import viewsets, status;
from rest_framework.decorators import action;
from rest_framework.response import Response;
from rest_framework.permissions import IsAuthenticated, AllowAny;
from rest_framework_simplejwt.views import TokenObtainPairView;
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer;

# local imports
from apps.authentication.models import User;
from apps.authentication.serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer;
from apps.authentication.permissions import IsSuperUser, IsCollegeAdminOrSuperUser;

# custom token serializer to add custom claims in the access token's payload (and return them in response)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user);
        
        # add custom claims
        token['role'] = user.role;
        token['email'] = user.email;
        token['college_id'] = user.college_id if user.college else None;
        return token;
    
    def validate(self, attrs):
        data = super().validate(attrs);
        
        # include extra data in response
        data.update(
            {
                'role': self.user.role,
                'email': self.user.email,
                'user_id': self.user.id,
                'college_id': self.user.college.id if self.user.college else None,
            }
        )
        
        return data;
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer;
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('college').all();
    serializer_class = UserSerializer;
    
    def get_permission(self):
        # All register endpoints to be used bu any if explicitly opened; otherwise require auth
        if self.action in ['create_public_student']:
            return [AllowAny()];
        
        if self.action in ['retrieve', 'list', 'partial_update', 'update', 'destroy']:
            return [IsAuthenticated(), IsCollegeAdminOrSuperUser()];
        
        return [IsAuthenticated()];
    
    def get_serializer_class(self):
        if self.action in ['create', 'create_public_student']:
            return CreateUserSerializer;
        
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer;
        
        return UserSerializer;
    
    # Superuser or College Admin can create users via standard create (e.g. create teacher/student)
    def create(self, request, *args, **kwargs):
        # only superuser or college admin should create users via this endpoint
        if not (request.user.role in ['superuser', 'college_admin']):
            return Response({'detail':'Only Superuser or college admin can create users here.'}, status= status.HTTP_403_FORBIDDEN);
        
        serializer = self.get_serializer(data=request.data);
        serializer.is_valid(raise_exception=True);
        
        user = serializer.save();
        
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED);
    
    @action(detail=False, methods=['post'], url_path='register-student-public', permission_classes=[AllowAny])
    def create_public_student(self, request):
        """
        Optional: allow public self-registration for students.
        If you don't want this, just ignore/delete this action.
        """
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)