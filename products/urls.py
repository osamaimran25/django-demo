from django.urls import path, include
from .views import ProductAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ProductAPIView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
