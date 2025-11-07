from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import College
from .serializers import CollegeSerializer, AssignCollegeAdminSerializer
from rest_framework.permissions import IsAuthenticated
from apps.authentication.permissions import IsSuperUser, IsCollegeAdminOrSuperUser
from apps.authentication.models import User

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def get_permissions(self):
        # create: only superuser
        if self.action == 'create':
            return [IsAuthenticated(), IsSuperUser()]
        # update: superuser or college admin (college admin only for their own college handled below)
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsCollegeAdminOrSuperUser()]
        # assign_admin: only superuser
        if self.action == 'assign_admin':
            return [IsAuthenticated(), IsSuperUser()]
        # list/retrieve: authenticated users can view; you may restrict further
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        # allow college_admin update only on their college: enforced at view level
        user = self.request.user
        if user.role == 'college_admin' and not user.is_superuser:
            # ensure the college being updated is the user's college
            if user.college is None or user.college.id != serializer.instance.id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("College admin can only modify their own college")
        serializer.save()

    @action(detail=True, methods=['post'], url_path='assign-admin')
    def assign_admin(self, request, pk=None):
        """
        Assign an existing user (role=college_admin) to this college
        Only superuser allowed.
        """
        college = self.get_object()
        serializer = AssignCollegeAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        user = User.objects.get(pk=user_id)
        user.college = college
        user.save()
        return Response({'detail': 'Assigned user as college admin for this college'})

