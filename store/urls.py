from django.urls import path, include
from rest_framework import routers
router=routers.DefaultRouter()
# ReferenceRequestTokensViewSet, ReferenceRequestsViewSet,
# router.register('document',WorkerDocumentViewSet , basename='workerdocuments')

urlpatterns=router.urls
urlpatterns=[
    path('',include(router.urls)),
]
