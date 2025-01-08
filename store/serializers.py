from datetime import datetime
import json
from uuid import UUID
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from store.fields import CustomDateTimeField
from . models import CustomUser, Order, OrderItem, Store,Product,Batch
from django.contrib.auth.models import  Group, Permission
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = (
            'groups',
            'user_permissions'
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password and len(password) < 8:
            raise serializers.ValidationError({"status":False,"data": "Password must be at least 8 characters long."})
        

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class logoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length = 400)


class StoreSerializer(serializers.ModelSerializer):
    # created_at = CustomDateTimeField()


    class Meta:
        model = Store
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    batches = BatchSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data


class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.UUIDField()
    quantity = serializers.IntegerField()
    batch = serializers.UUIDField()
    
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)

class CreateOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    customer_email = serializers.EmailField()
    status = serializers.CharField(max_length=50, required= False)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    orderItems = serializers.ListField()
    store = serializers.UUIDField()
    shop_name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=2555, required=False)
    date_issued = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        store = Store.objects.get(id = validated_data['store'])
        items_data = validated_data.pop('orderItems')
        order = Order.objects.create(
            customer_name=validated_data['customer_name'],
            customer_email=validated_data['customer_email'],
            store = store,
            status=validated_data.get('status', 'pending'),
            shop_name=validated_data.get('shop_name', None),
            description=validated_data.get('description', None),
            date_issued=validated_data.get('date_issued', datetime.now().date)
        )

        total_amount = 0
     
        for item_data in json.loads(items_data[0]):
            item = OrderItem.objects.create(
                order=order,
                product_id=item_data['id'],
                batch_id=item_data.get('batch', None),
                quantity=item_data.get('quantity', 1),
                price_per_unit=item_data.get('price', 1),
                subtotal=item_data.get('subtotal', 0)
            )
            
            total_amount += float(item.subtotal)

        order.total_amount = total_amount
        order.save()
        return order


