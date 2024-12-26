from django.urls import path, include
from rest_framework import routers

from store import views

router=routers.DefaultRouter()
router.register('auth', views.AuthViewSet, basename='auth')
router.register('store', views.StoreViewSet, basename='store')
router.register('user', views.UserViewSet, basename='user')
router.register('get_user_from_token',views.UserTokenViewSet, basename='user_token')
router.register('product', views.ProductViewSet, basename='product')
router.register('batch', views.BatchViewSet, basename='batch')
router.register('order', views.OrderViewSet, basename='order')

urlpatterns=router.urls
urlpatterns=[
    path('',include(router.urls)),
]
