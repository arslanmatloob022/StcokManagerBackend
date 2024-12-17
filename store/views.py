from store.models import CustomUser, Store
from store import serializers
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from .services.authenciation_service import AuthenticationService
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class AuthViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=('POST',),
        url_path='login',
        serializer_class=serializers.LoginSerializer,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email, password = (
            serializer.validated_data['email'],
            serializer.validated_data['password'],
        )

        access_token, refresh_token, user = AuthenticationService.login(email, password, is_superuser=False)

        return Response(
            data={
                'access': access_token,
                'refresh': refresh_token,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    

    
    @action(
        detail=False,
        methods=('POST',),
        url_path='logout',
        serializer_class=serializers.logoutSerializer,
        permission_classes=([IsAuthenticated])

    )
    def logout_user(self, request):
        """Blacklist the refresh token: extract token from the header
        during logout request user and refresh token is provided"""
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
     
        return Response("Successful Logout", status=status.HTTP_200_OK)

class UserTokenViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        email = self.request.user.email
        queryset = CustomUser.objects.filter(email=email)
        return queryset
    


class UserViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = ([IsAuthenticated ])
    http_method_names = ['get','post','put', 'delete','patch']


class StoreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer
    permission_classes = ([IsAuthenticated ])
