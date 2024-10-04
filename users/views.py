from rest_framework import generics, status
from rest_framework.response import Response
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from users.serializers import (UserRegisterSerializer, UserLogoutSerializer,
                               UserSerializer, UserProfileSerializer
                               )


# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(operation_summary="Get user profile")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'username': user.username}, status=status.HTTP_201_CREATED)


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status': 'success',
            'detail': "Logged out successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
