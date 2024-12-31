from store.models import Batch, CustomUser, Order, Product, Store
from store import serializers
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from .services.authenciation_service import AuthenticationService
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.parsers import FormParser, MultiPartParser


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

        access_token, refresh_token, user = AuthenticationService.login(email, password)

        return Response(
            data={
                'access': access_token,
                'refresh': refresh_token,
                'user': serializers.UserSerializer(user).data,
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

class ProductViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = ([IsAuthenticated ])
    parser_classes=(FormParser, MultiPartParser)


    @action(detail=False, methods=['get'], url_path='store/(?P<store>[a-f0-9-]{36})', permission_classes=[IsAuthenticated], serializer_class = serializers.ProductSerializer)
    def get_store_products(self, request, store, *args, **kwargs):
        products = Product.objects.filter(store=store)
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('GET',),
        url_path='batches',
        permission_classes=([IsAuthenticated])
    )
    def get_batches(self, request, pk):
        product = Product.objects.get(pk=pk)
        batches = Batch.objects.filter(product=product)
        serializer = serializers.BatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(
        detail=True,
        methods=('GET',),
        url_path='details', 
        permission_classes=[IsAuthenticated]
    )
    def get_product_details(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = serializers.ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BatchViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Batch.objects.all()
    serializer_class = serializers.BatchSerializer
    permission_classes = ([IsAuthenticated ])



class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = ([IsAuthenticated ])


    @action(detail=False, methods=['get'], url_path='store/(?P<store>[a-f0-9-]{36})', permission_classes=[IsAuthenticated], serializer_class = serializers.OrderSerializer)
    def get_store_orders(self, request, store, *args, **kwargs):
        orders = Order.objects.filter(store=store)
        data = serializers.OrderSerializer(orders, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='create-order', permission_classes=[IsAuthenticated], serializer_class = serializers.CreateOrderSerializer)
    def create_order(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Order created successfully."}, status=status.HTTP_201_CREATED)


    




    