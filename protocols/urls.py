from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, IndicationViewSet, SaveProtocolView, MyProtocolsView, ProtocolRequestView

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'indications', IndicationViewSet, basename='indication')

urlpatterns = [
    path('', include(router.urls)),
    path('save/', SaveProtocolView.as_view(), name='save-protocol'),
    path('my-protocols/', MyProtocolsView.as_view(), name='my-protocols'),
    path('protocol-request/', ProtocolRequestView.as_view(), name='protocol-request'),
]
